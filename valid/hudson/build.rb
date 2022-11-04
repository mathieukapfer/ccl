#!/usr/bin/ruby
#
# Copyright (C) 2008-2021 Kalray SA.
#
# All rights reserved.
#

$LOAD_PATH.push('metabuild/lib')
require 'metabuild'
include Metabuild
require 'qualityChecker'

options = Options.new({
            "clone"         => ".",
            "toolroot"      => ["kEnv/kvxtools/opt/kalray/accesscore", "Prefix to available tools."],
            "kalrayReq"     => ["kEnv/kvxtools/opt/kalray/kalrayReq/", "Path to kalrayReq env containing latex stuff."],
            "artifacts"     => {"type" => "string", "default" => "artifacts", "help" => "Artifacts path given by Jenkins."},
            "report_path"   => {"type" => "string", "default" => "report_path", "help" => "Report path given by Jenkins."},

            "build_type" => {
                "type"      => "keywords",
                "keywords"  => [:Release, :Debug],
                "default"   => "Release",
                "help"      => "Release type"
            },
            "board" => {
                "type"      => "keywords",
                "keywords"  => [:csp_generic],
                "default"   => "csp_generic",
                "help"      => "Target board (changing things at compilation)."
            },
            "execution_platform" => {
                "type"      => "keywords",
                "keywords"  => [:hw, :sim],
                "default"   => "hw",
                "help"      => "Execution platform: can be hardware (jtag, PCI) or simulation (kvx-mppa, kvx-cluster)."
            },
            "version"       => "Top repo version for packaging",
            "step"          => {"type" => "string", "default" => "", "help" => "Jenkinsfile step name, used to specify current step when pipeline is split into several steps."},
})

# Repository
workspace   = options["workspace"]
branch      = options["branch"]
clone       = options["clone"]
repo        = Git.new(clone, workspace)

# Tools and build params
toolroot          = File.expand_path(options["toolroot"], workspace)
kvxtools          = File.expand_path(options["toolroot"])
kalrayReq         = File.expand_path(options["kalrayReq"])
artifacts         = File.expand_path(options["artifacts"])
report_path       = File.expand_path(options["report_path"])
step              = options["step"]
build_type        = options["build_type"]
prefix            = File.expand_path(options["prefix"], workspace)
module_label      = clone.dup.to_s
module_path       = File.join(workspace, clone)
module_build_path = File.join(module_path, "build")

# Sanity check
if !File.exists?(toolroot) then
    raise "Can not find toolroot " + toolroot + "\n"
end

# Module developpment images directories
module_devimage = {
    runtime:       File.join(module_path, "devimage-runtime"),
    doc_src:       File.join(module_path, "devimage-doc-src"),
    tests:         File.join(module_path, "devimage-tests"),
}

# Module packages names
package_label = module_label.dup.gsub("_", "-").downcase
module_pkg_name = {
    runtime:       "kalray-accesscore-#{package_label}",
    doc_src:       "kalray-accesscore-#{package_label}-doc-src",
    tests:         "kalray-accesscore-#{package_label}-tests",
}

# Sanity check
if module_devimage.size != module_pkg_name.size or !(module_devimage.keys - module_pkg_name.keys).empty? then
    raise "module_devimage and module_pkg_name must have same keys"
end

# Module tests directories
module_tests_prefix = File.join(module_devimage[:tests], module_pkg_name[:tests]) # Where to install tests
module_tests_path   = File.join(toolroot, module_pkg_name[:tests])                # Where to run tests

# Execution
board              = options["board"].to_s
execution_platform = options["execution_platform"].to_s

# Builder targets
clean       = Target.new("clean", repo, [])
check       = Target.new("check", repo, [])
build       = ParallelTarget.new("build", repo, [])
install     = Target.new("install", repo, [])
package     = Target.new("package", repo, [])
valid_accel = Target.new("valid_accel", repo, [])
valid_std   = Target.new("valid_std", repo, [])
report_perf = Target.new("report_perf", repo, [])

# Top builder
$builder = Builder.new(clone, options, [clean, check, build, install, package, valid_accel, valid_std, report_perf])
$builder.default_targets = [package]
$builder.set_default_package_dir(File.join(workspace, "packages"))

# Must use the release_info from the top repo, not the sub-module itself
# (version, releaseID, sha1) = repo.describe()
# release_info = $builder.release_info(version, releaseID, sha1)
(version, buildID) = options["version"].split("-")
release_info = $builder.release_info(version, buildID)

# Build environment
env = {}
env["KALRAY_TOOLCHAIN_DIR"] = kvxtools
env["PATH"] = "#{kvxtools}/bin:#{ENV["PATH"]}"
env["LD_LIBRARY_PATH"] = "#{kvxtools}/lib:#{ENV["LD_LIBRARY_PATH"]}"
env["POCL_CACHE_DIR"]  = "#{module_path}/.pocl_cache_dir/"
env["PKG_CONFIG_PATH"] = "#{toolroot}/lib/pkgconfig:#{ENV["PKG_CONFIG_PATH"]}"

# Directories to inspect with code checker
code_checks_directories = ["src"]

$builder.target("check") do
    $builder.logtitle = "Report for #{module_label} check"
    raise "artifacts option not set" if(artifacts.empty?)
    mkdir_p module_build_path
    code_perf_file = File.join(module_build_path, "#{module_label}_code_checks.perf")

    # Only do check once over targets dependencies
    if !File.exists?(code_perf_file) then
        mkdir_p module_build_path
        cd module_path

        qc = QualityChecker.new($builder, kalrayReq)
        qc.code_checks(code_checks_directories, code_perf_file, "--CCN 45 --length 250", "", "", 60, "false")

        # Publish code_checks reporting
        cd workspace
        $builder.report_perf_files("#{module_label}_code_checks", [code_perf_file])

        cd ".metabuild"
        if File.exists?("perffiles") then
            mkdir_p artifacts
            cd "perffiles"
            $builder.run("tar -cvf perffiles.tar *.perf")
            $builder.run("mv perffiles.tar #{artifacts}")
        end
    end
end

$builder.target("clean") do
    $builder.logtitle = "Report for #{module_label} clean"
    cd module_path

    FileUtils.rm_rf module_build_path
    module_devimage.each_value do |devimage|
        FileUtils.rm_rf devimage
    end
end

$builder.target("build") do
    $builder.logtitle = "Report for #{module_label} build"
    cd module_path

    # Doc
    cmd = "make -f Makefile.doc O=#{module_build_path}/doc all"
    $builder.run(:env => env, :cmd => cmd)
end

$builder.target("install") do
    $builder.logtitle = "Report for #{module_label} install"
    module_devimage.each_value do |devimage|
        mkdir_p devimage
    end
    cd module_path

    # Install Python scripts
    python_path = File.join(module_devimage[:runtime], "share", module_label, "src")
    mkdir_p python_path
    cmd = "cp -r src/* #{python_path}"
    $builder.run(:env => env, :cmd => cmd)

    # Install helper
    cmd = "install -m 744 get_pipenv_path #{python_path}/.."
    $builder.run(:env => env, :cmd => cmd)

    # Install binary wrapper
    bin_path = File.join(module_devimage[:runtime], "bin")
    mkdir_p bin_path
    cmd = "install -m 744 ccl_viewer #{bin_path}"
    $builder.run(:env => env, :cmd => cmd)
    cmd = "install -m 744 ccl_parser #{bin_path}"
    $builder.run(:env => env, :cmd => cmd)

    # Install doc sources
    cmd = "make -f Makefile.doc O=#{module_build_path}/doc PREFIX=#{module_devimage[:doc_src]}/ install-doc-src"
    $builder.run(:env => env, :cmd => cmd)

end

$builder.target("package") do
    $builder.logtitle = "Report for #{module_label} package"

    # Runtime package
    depends = []
    $builder.create_package_with_files(
        :name => module_pkg_name[:runtime],
        :desc => "CCL file tools: parse CCL file and display graphical view\n",
        :license => "Kalray",
        :release_info => release_info,
        :depends => depends,
        :pkg_files => { module_devimage[:runtime] => "/opt/kalray/accesscore" },
    )

    # Doc sources package
    depends = []
    $builder.add_depend(module_pkg_name[:runtime], depends)
    $builder.create_package_with_files(
        :name => module_pkg_name[:doc_src],
        :desc => "CCL file tools: parse CCL file and display graphical view - doc src\n",
        :license => "Kalray",
        :release_info => release_info,
        :depends => depends,
        :pkg_files => { module_devimage[:doc_src] => "/opt/kalray/accesscore" },
    )

end

$builder.target("valid_accel") do
    $builder.logtitle = "Report for #{module_label} valid_accel"
    mkdir_p File.join(artifacts, module_label)
    mkdir_p report_path
end

$builder.target("valid_std") do
    $builder.logtitle = "Report for #{module_label} valid_std"
    mkdir_p File.join(artifacts, module_label)
    mkdir_p report_path
end

$builder.target("report_perf") do
    $builder.logtitle = "Report for #{module_label} report_perf"
    raise "artifacts option not set" if(artifacts.empty?)
    mkdir_p File.join(artifacts, module_label)

    # Module report perf file
    perf_file = File.join(artifacts, module_label, "#{module_label}.perf")

    # Automatic parsing logs on the format: "#<label>=<value> <unit>"
    open(perf_file, "a") do |output_file| # Append mode
        Dir.glob(File.join(artifacts, module_label, "*.log")).each do |benche|
            benche_file = File.readlines(benche).select { |line| line =~ /^#.*=.*/ }
            benche_file.each do |line|
                parse = line.split("=")
                metric_unit = parse[1].split(" ")[1]
                metric_label = parse[0].gsub("#", "")
                metric_value = parse[1].split(" ")[0]

                output_file << "#{metric_unit} #{metric_label} #{metric_value}\n"
            end
        end
    end

    $builder.report_perf_files(clone, [perf_file])
end

$builder.launch()
