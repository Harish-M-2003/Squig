; ModuleID = "main"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
entry:
  %"a" = alloca i32
  store i32 5, i32* %"a"
  %".3" = load i32, i32* %"a"
  %".4" = add i32 %".3", 5
  %"b" = alloca i32
  store i32 %".4", i32* %"b"
  ret i32 %".4"
}
