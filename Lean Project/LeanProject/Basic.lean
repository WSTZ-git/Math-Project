/-!
# 公共定义与记号

各课题共用的定义、记号与基础引理。新模块请先 `import LeanProject.Basic`。
-/

namespace LeanProject

/-- 占位定义，可删除。 -/
def hello : String := "world"

/-- 测试：加法交换律 -/
example (a b : Nat) : a + b = b + a := Nat.add_comm a b

end LeanProject
