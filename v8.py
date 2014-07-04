# Offsets for different classes of overhead
kOffsetCrankShaftTypeChecks = 0
kOffsetRuntimeCalls = 1000
kOffsetJSRuntimeCalls = 2000
kOffsetUnknownRuntimeCalls = 3000
kOffsetInlinedCacheHandlersDetailed = 4000
kOffsetInlinedCacheCalls = 5000
kOffsetFullCompilerChecks = 6000

def getCrankShaftTypeCheckNames():
  return (
    "UsefulWork", 
    "Smi",
    "Overflow",
    "ShiftOverflow",
    "DivByZero",
    "MinusZero",
    "Remainder",
    "Condition",
    "Hole",
    "Prototype",
    "Polymorphic",
    "Function",
    "Argument",
    "Unsigned",
    "Receiver",
    "ArgumentLimit",
    "IsHeapNumber",
    "MathAbs",
    "FloorOverflow",
    "RoundOverflow",
    "Power",
    "Bounds",
    "XMM",
    "InstanceType",
    "FunctionTarget",
    "Map",
    "ElementsKind",
    "ForInMap",
    "ForInArray",
    "MapValue",
    "CheckDate",
    "WriteBarrier",
  )

def getFullCompilerCheckNames():
  return (
    "LoadField",
    "LoadArrayLength",
    "LoadStringLength",
    "LoadFunctionPrototype",
    "LoadConstant",
    "LoadInterceptor",
    "LoadGlobal",
    "LoadElement",
    "LoadPolymorphic",
    "LoadNonexistent",
    "LoadCallback",
    "LoadViaGetter",
    "LoadDictionaryElement",
    "LoadExternalArray",
    "LoadFastElement",
    "LoadFastDoubleElement",
    "StoreField",
    "StoreInterceptor",
    "StoreGlobal",
    "StoreElement",
    "StorePolymorphic",
    "StoreCallback",
    "StoreViaSetter",
    "StoreExternalArray",
    "StoreFastElement",
    "StoreFastDoubleElement",
    "CallField",
    "CallConstant",
    "CallInterceptor",
    "CallGlobal",
    "ArrayPushCall",
    "ArrayPopCall",
    "StringCharCodeAtCall",
    "StringCharAtCall",
    "StringFromCharCodeCall",
    "MathFloorCall",
    "MathAbsCall",
    "Probe",
    "FastApiCall",
  )

def getInlinedCacheCallNames():
  return (
    "LoadIC_Miss",
    "KeyedLoadIC_Miss",
    "KeyedLoadIC_MissForceGeneric",
    "CallIC_Miss",
    "KeyedCallIC_Miss",
    "StoreIC_Miss",
    "StoreIC_ArrayLength",
    "SharedStoreIC_ExtendStorage",
    "KeyedStoreIC_Miss",
    "KeyedStoreIC_MissForceGeneric",
    "KeyedStoreIC_Slow",
    "LoadCallbackProperty",
    "StoreCallbackProperty",
    "LoadPropertyWithInterceptorOnly",
    "LoadPropertyWithInterceptorForLoad",
    "LoadPropertyWithInterceptorForCall",
    "KeyedLoadPropertyWithInterceptor",
    "StoreInterceptorProperty",
    "UnaryOp_Patch",
    "BinaryOp_Patch",
    "CompareIC_Miss",
    "ToBoolean_Patch",
  )

def getInlinedCacheHandlerDetailedNames():
  return (
    "LoadIC_Initialize",
    "KeyedLoadIC_Initialize",
    "StoreIC_Initialize",
    "KeyedStoreIC_Initialize",
    "LoadIC_PreMonomorphic",
    "KeyedLoadIC_PreMonomorphic",
  )

def getRuntimeCallNames():
  return (
    "GetProperty",
    "KeyedGetProperty",
    "DeleteProperty",
    "HasLocalProperty",
    "HasProperty",
    "HasElement",
    "IsPropertyEnumerable",
    "GetPropertyNames",
    "GetPropertyNamesFast",
    "GetLocalPropertyNames",
    "GetLocalElementNames",
    "GetInterceptorInfo",
    "GetNamedInterceptorPropertyNames",
    "GetIndexedInterceptorElementNames",
    "GetArgumentsProperty",
    "ToFastProperties",
    "FinishArrayPrototypeSetup",
    "SpecialArrayFunctions",
    "GetDefaultReceiver",
    "GetPrototype",
    "IsInPrototypeChain",
    "GetOwnProperty",
    "IsExtensible",
    "PreventExtensions",
    "CheckIsBootstrapping",
    "GetRootNaN",
    "Call",
    "Apply",
    "GetFunctionDelegate",
    "GetConstructorDelegate",
    "NewArgumentsFast",
    "NewStrictArgumentsFast",
    "LazyCompile",
    "LazyRecompile",
    "ParallelRecompile",
    "NotifyDeoptimized",
    "NotifyOSR",
    "DeoptimizeFunction",
    "ClearFunctionTypeFeedback",
    "RunningInSimulator",
    "OptimizeFunctionOnNextCall",
    "GetOptimizationStatus",
    "GetOptimizationCount",
    "CompileForOnStackReplacement",
    "SetNewFunctionAttributes",
    "AllocateInNewSpace",
    "SetNativeFlag",
    "StoreArrayLiteralElement",
    "DebugCallbackSupportsStepping",
    "DebugPrepareStepInIfStepping",
    "PushIfAbsent",
    "ArrayConcat",
    "ToBool",
    "Typeof",
    "StringToNumber",
    "StringFromCharCodeArray",
    "StringParseInt",
    "StringParseFloat",
    "StringToLowerCase",
    "StringToUpperCase",
    "StringSplit",
    "CharFromCode",
    "URIEscape",
    "URIUnescape",
    "QuoteJSONString",
    "QuoteJSONStringComma",
    "QuoteJSONStringArray",
    "NumberToString",
    "NumberToStringSkipCache",
    "NumberToInteger",
    "NumberToIntegerMapMinusZero",
    "NumberToJSUint32",
    "NumberToJSInt32",
    "NumberToSmi",
    "AllocateHeapNumber",
    "NumberAdd",
    "NumberSub",
    "NumberMul",
    "NumberDiv",
    "NumberMod",
    "NumberUnaryMinus",
    "NumberAlloc",
    "StringAdd",
    "StringBuilderConcat",
    "StringBuilderJoin",
    "SparseJoinWithSeparator",
    "NumberOr",
    "NumberAnd",
    "NumberXor",
    "NumberNot",
    "NumberShl",
    "NumberShr",
    "NumberSar",
    "NumberEquals",
    "StringEquals",
    "NumberCompare",
    "SmiLexicographicCompare",
    "StringCompare",
    "Math_acos",
    "Math_asin",
    "Math_atan",
    "Math_atan2",
    "Math_ceil",
    "Math_cos",
    "Math_exp",
    "Math_floor",
    "Math_log",
    "Math_pow",
    "Math_pow_cfunction",
    "RoundNumber",
    "Math_sin",
    "Math_sqrt",
    "Math_tan",
    "RegExpCompile",
    "RegExpExec",
    "RegExpExecMultiple",
    "RegExpInitializeObject",
    "RegExpConstructResult",
    "ParseJson",
    "StringCharCodeAt",
    "StringIndexOf",
    "StringLastIndexOf",
    "StringLocaleCompare",
    "SubString",
    "StringReplaceRegExpWithString",
    "StringReplaceOneCharWithString",
    "StringMatch",
    "StringTrim",
    "StringToArray",
    "NewStringWrapper",
    "NumberToRadixString",
    "NumberToFixed",
    "NumberToExponential",
    "NumberToPrecision",
    "FunctionSetInstanceClassName",
    "FunctionSetLength",
    "FunctionSetPrototype",
    "FunctionSetReadOnlyPrototype",
    "FunctionGetName",
    "FunctionSetName",
    "FunctionNameShouldPrintAsAnonymous",
    "FunctionMarkNameShouldPrintAsAnonymous",
    "FunctionBindArguments",
    "BoundFunctionGetBindings",
    "FunctionRemovePrototype",
    "FunctionGetSourceCode",
    "FunctionGetScript",
    "FunctionGetScriptSourcePosition",
    "FunctionGetPositionForOffset",
    "FunctionIsAPIFunction",
    "FunctionIsBuiltin",
    "GetScript",
    "CollectStackTrace",
    "GetV8Version",
    "ClassOf",
    "SetCode",
    "SetExpectedNumberOfProperties",
    "CreateApiFunction",
    "IsTemplate",
    "GetTemplateField",
    "DisableAccessChecks",
    "EnableAccessChecks",
    "DateCurrentTime",
    "DateParseString",
    "DateLocalTimezone",
    "DateToUTC",
    "DateMakeDay",
    "DateSetValue",
    "CompileString",
    "GlobalPrint",
    "GlobalReceiver",
    "ResolvePossiblyDirectEval",
    "SetProperty",
    "DefineOrRedefineDataProperty",
    "DefineOrRedefineAccessorProperty",
    "IgnoreAttributesAndSetProperty",
    "RemoveArrayHoles",
    "GetArrayKeys",
    "MoveArrayContents",
    "EstimateNumberOfElements",
    "LookupAccessor",
    "MaterializeRegExpLiteral",
    "CreateObjectLiteral",
    "CreateObjectLiteralShallow",
    "CreateArrayLiteral",
    "CreateArrayLiteralShallow",
    "IsJSModule",
    "CreateJSProxy",
    "CreateJSFunctionProxy",
    "IsJSProxy",
    "IsJSFunctionProxy",
    "GetHandler",
    "GetCallTrap",
    "GetConstructTrap",
    "Fix",
    "SetInitialize",
    "SetAdd",
    "SetHas",
    "SetDelete",
    "MapInitialize",
    "MapGet",
    "MapHas",
    "MapDelete",
    "MapSet",
    "WeakMapInitialize",
    "WeakMapGet",
    "WeakMapHas",
    "WeakMapDelete",
    "WeakMapSet",
    "NewClosure",
    "NewObject",
    "NewObjectFromBound",
    "FinalizeInstanceSize",
    "Throw",
    "ReThrow",
    "ThrowReferenceError",
    "ThrowNotDateError",
    "StackGuard",
    "Interrupt",
    "PromoteScheduledException",
    "NewGlobalContext",
    "NewFunctionContext",
    "PushWithContext",
    "PushCatchContext",
    "PushBlockContext",
    "PushModuleContext",
    "DeleteContextSlot",
    "LoadContextSlot",
    "LoadContextSlotNoReferenceError",
    "StoreContextSlot",
    "DeclareGlobals",
    "DeclareContextSlot",
    "InitializeVarGlobal",
    "InitializeConstGlobal",
    "InitializeConstContextSlot",
    "OptimizeObjectForAddingMultipleProperties",
    "DebugPrint",
    "DebugTrace",
    "TraceEnter",
    "TraceExit",
    "Abort",
    "Log",
    "LocalKeys",
    "GetFromCache",
    "NewMessageObject",
    "MessageGetType",
    "MessageGetArguments",
    "MessageGetStartPosition",
    "MessageGetScript",
    "IS_VAR",
    "HasFastSmiElements",
    "HasFastSmiOrObjectElements",
    "HasFastObjectElements",
    "HasFastDoubleElements",
    "HasFastHoleyElements",
    "HasDictionaryElements",
    "HasExternalPixelElements",
    "HasExternalArrayElements",
    "HasExternalByteElements",
    "HasExternalUnsignedByteElements",
    "HasExternalShortElements",
    "HasExternalUnsignedShortElements",
    "HasExternalIntElements",
    "HasExternalUnsignedIntElements",
    "HasExternalFloatElements",
    "HasExternalDoubleElements",
    "HasFastProperties",
    "TransitionElementsSmiToDouble",
    "TransitionElementsDoubleToObject",
    "HaveSameMap",
    "ProfilerResume",
    "ProfilerPause",
    "BeginSimulation",
    "EndSimulation",
    "ExitSimulation",
    "MarkFullFunctionEnter",
    "MarkFullFunctionExit",
    "MarkCrankShaftFunctionEnter",
    "MarkCrankShaftFunctionExit",
  )

def isUsefulWork(type):
  return int(type) == 0

def isCrankShaftTypeCheck(type):
  return int(type) >= kOffsetCrankShaftTypeChecks and int(type) < kOffsetCrankShaftTypeChecks + 1000

def isRuntimeCall(type):
  return int(type) >= kOffsetRuntimeCalls and int(type) < kOffsetRuntimeCalls + 1000

def isJSRuntimeCall(type):
  return int(type) >= kOffsetJSRuntimeCalls and int(type) < kOffsetJSRuntimeCalls + 1000

def isUnknownRuntimeCall(type):
  return int(type) >= kOffsetUnknownRuntimeCalls and int(type) < kOffsetUnknownRuntimeCalls + 1000

def isInlinedCacheHandlerDetailed(type):
  return int(type) >= kOffsetInlinedCacheHandlersDetailed and int(type) < kOffsetInlinedCacheHandlersDetailed + 1000

def isInlinedCacheCall(type):
  return int(type) >= kOffsetInlinedCacheCalls and int(type) < kOffsetInlinedCacheCalls + 1000

def isFullCompilerCheck(type):
  return int(type) >= kOffsetFullCompilerChecks and int(type) < kOffsetFullCompilerChecks + 1000

def isCheckOverhead(type):
  return isCrankShaftTypeCheck(type) or isFullCompilerCheck(type)

def isRuntimeOverhead(type):
  return isRuntimeCall(type) or isJSRuntimeCall(type) or isUnknownRuntimeCall(type)

def getTypeName(type):
  if isUsefulWork(type):
    return "UsefulWork"
  if isCrankShaftTypeCheck(type):
    return "OptCheck_" + getCrankShaftTypeCheckNames()[type]
  if isFullCompilerCheck(type):
    return "FullCheck_" + getFullCompilerCheckNames()[type - kOffsetFullCompilerChecks]
  if isRuntimeCall(type):
    return "C_" + getRuntimeCallNames()[type - kOffsetRuntimeCalls]
  if isJSRuntimeCall(type):
    return "JS_Runtime"
  if isUnknownRuntimeCall(type):
    return "C_Unknown_Runtime"
  if isInlinedCacheHandlerDetailed(type):
    return "IC_" + getInlinedCacheHandlerDetailedNames()[type - kOffsetInlinedCacheHandlersDetailed]
  if isInlinedCacheCall(type):
    return "IC_" + getInlinedCacheCallNames()[type - kOffsetInlinedCacheCalls]
  return "Unknown"

def getTypeNames():
  typeNames = ["UsefulWork"]
  for typeName in getCrankShaftTypeCheckNames():
    typeNames.append("OptCheck_" + typeName)
  for typeName in getFullCompilerCheckNames():
    typeNames.append("FullCheck_" + typeName)
  for typeName in getInlinedCacheHandlerDetailedNames():
    typeNames.append("IC_" + typeName)
  for typeName in getInlinedCacheCallNames():
    typeNames.append("IC_" + typeName)
  typeNames.append("Unknown")
  for typeName in getRuntimeCallNames():
    typeNames.append("C_" + typeName)
  typeNames.append("JS_Runtime")
  typeNames.append("C_Unknown_Runtime")
  typeNames.append("Misc")
  return typeNames

def getTypeNamesMissesOnly():
  typeNames = ["UsefulWork"]
  typeNames.append("Checks")
  for typeName in getInlinedCacheCallNames():
    typeNames.append("IC_" + typeName)
  typeNames.append("C_" + "CreateObjectLiteral")
  typeNames.append("C_" + "CreateObjectLiteralShallow")
  typeNames.append("C_" + "CreateArrayLiteral")
  typeNames.append("C_" + "CreateArrayLiteralShallow")
  typeNames.append("Runtime")
  return typeNames

def getAggregatedCrankShaftTypeCheckName(type):
  name = getCrankShaftTypeCheckNames()[type]
  if name == "UsefulWork":
    return name
  else:
    return "CrankshaftChecks"

def getAggregatedRuntimeCallName(type):
  if isUnknownRuntimeCall(type):
    return "Library"
  if len(getRuntimeCallNames()) <= type - kOffsetRuntimeCalls:
    return "Library"
  name = getRuntimeCallNames()[type - kOffsetRuntimeCalls]
  if name == "LazyCompile" or name == "LazyRecompile":
    return "Compiler"
  else:
    return "Library"

def getAggregatedTypeName(type):
  if isCrankShaftTypeCheck(type):
    return getAggregatedCrankShaftTypeCheckName(type)
  if isFullCompilerCheck(type):
    return "FullCompilerChecks"
  if isRuntimeCall(type) or isUnknownRuntimeCall(type):
    return "Runtime" + getAggregatedRuntimeCallName(type)
  if isJSRuntimeCall(type):
    return "JS_Runtime"
  if isInlinedCacheHandlerDetailed(type) or isInlinedCacheCall(type):
    return "IC_Runtime"
  return "Unknown"

def getAggregatedTypeNames():
  return (
      "UsefulWork",
      "CrankshaftChecks",
      "FullCompilerChecks",
      "IC_Runtime",
      "Unknown",
      "RuntimeCompiler",
      "RuntimeLibrary",
      "JS_Runtime",
      "Misc"
  )
