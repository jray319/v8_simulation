gc();
load("./benchmarks/sunspider-0.9.1/3d-morph.js");
runBenchmark();
runBenchmark();
runBenchmark();
gc();
print("PROFILE BEGIN");
%EnterSimulation();
%BeginSimulation();
runBenchmark();
%EndSimulation();
%ExitSimulation();
