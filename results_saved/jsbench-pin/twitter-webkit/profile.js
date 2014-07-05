gc();
load("./benchmarks/jsbench-2012.1/twitter-webkit.js");
print("PROFILE BEGIN");
%EnterSimulation();
%BeginSimulation();
run_simulation();
%EndSimulation();
%ExitSimulation();
