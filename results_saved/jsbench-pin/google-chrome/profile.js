gc();
load("./benchmarks/jsbench-2012.1/google-chrome.js");
print("PROFILE BEGIN");
%EnterSimulation();
%BeginSimulation();
run_simulation();
%EndSimulation();
%ExitSimulation();
