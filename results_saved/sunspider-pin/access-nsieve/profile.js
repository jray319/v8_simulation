gc();
load("./benchmarks/sunspider-0.9.1/access-nsieve.js");
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
