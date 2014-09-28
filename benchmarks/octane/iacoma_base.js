// A benchmark has a name (string) and a function that will be run to
// do the performance measurement. The optional setup and tearDown
// arguments are functions that will be invoked before and after
// running the benchmark, but the running time of these functions will
// not be accounted for in the benchmark score.
function Benchmark(name, doWarmup, doDeterministic, deterministicIterations, 
                   run, setup, tearDown, rmsResult, minIterations) {
  this.name = name;
  this.doWarmup = doWarmup;
  this.doDeterministic = doDeterministic;
  this.deterministicIterations = deterministicIterations;
  this.run = run;
  this.Setup = setup ? setup : function() { };
  this.TearDown = tearDown ? tearDown : function() { };
  this.rmsResult = rmsResult ? rmsResult : null; 
  this.minIterations = minIterations ? minIterations : 32;
}


// Suites of benchmarks consist of a name and the set of benchmarks in
// addition to the reference timing that the final score will be based
// on. This way, all scores are relative to a reference run and higher
// scores implies better performance.
function BenchmarkSuite(name, reference, benchmarks) {
  this.name = name;
  this.reference = reference;
  this.benchmarks = benchmarks;
  BenchmarkSuite.suites.push(this);
}


// Keep track of all declared benchmark suites.
BenchmarkSuite.suites = [];


// Override the alert function to throw an exception instead.
alert = function(s) {
  throw "Alert called with argument: " + s;
};


// To make the benchmark results predictable, we replace Math.random
// with a 100% deterministic alternative.
BenchmarkSuite.ResetRNG = function() {
  Math.random = (function() {
    var seed = 49734321;
    return function() {
      // Robert Jenkins' 32 bit integer hash function.
      seed = ((seed + 0x7ed55d16) + (seed << 12))  & 0xffffffff;
      seed = ((seed ^ 0xc761c23c) ^ (seed >>> 19)) & 0xffffffff;
      seed = ((seed + 0x165667b1) + (seed << 5))   & 0xffffffff;
      seed = ((seed + 0xd3a2646c) ^ (seed << 9))   & 0xffffffff;
      seed = ((seed + 0xfd7046c5) + (seed << 3))   & 0xffffffff;
      seed = ((seed ^ 0xb55a4f09) ^ (seed >>> 16)) & 0xffffffff;
      return (seed & 0xfffffff) / 0x10000000;
    };
  })();
}


// Override the random function.
BenchmarkSuite.ResetRNG();


function setup_func() {
  print("[SETUP]");
  for(var i = 0; i < BenchmarkSuite.suites.length; ++i) {
    var suite = BenchmarkSuite.suites[i];
    print('Suite: ' + suite.name);
    for(var j = 0; j < suite.benchmarks.length; ++j) {
      var benchmark = suite.benchmarks[j];
      print('  Benchmark: ' + benchmark.name);
      benchmark.Setup();
    }
  }
}


function run_func() {
  print("[RUN]");
  for(var i = 0; i < BenchmarkSuite.suites.length; ++i) {
    var suite = BenchmarkSuite.suites[i];
    print('Suite: ' + suite.name);
    for(var j = 0; j < suite.benchmarks.length; ++j) {
      var benchmark = suite.benchmarks[j];
      print('  Benchmark: ' + benchmark.name);
      benchmark.run();
    }
  }
}


function teardown_func() {
  print("[TEARDOWN]");
  for(var i = 0; i < BenchmarkSuite.suites.length; ++i) {
    var suite = BenchmarkSuite.suites[i];
    print('Suite: ' + suite.name);
    for(var j = 0; j < suite.benchmarks.length; ++j) {
      var benchmark = suite.benchmarks[j];
      print('  Benchmark: ' + benchmark.name);
      benchmark.TearDown();
    }
  }
}
