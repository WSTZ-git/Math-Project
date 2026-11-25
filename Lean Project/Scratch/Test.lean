import Mathlib

/-!
# Mathlib 用法示例

两种引入方式：
  import Mathlib                    全部内容（本例，最省事，首次加载慢）
  import Mathlib.Analysis.Calculus.Deriv.Pow   只要某个模块（最快）

用 `lake env lean Scratch/Test.lean` 检查。
-/

-- 查定理的类型
#check Continuous.comp
#check Real.sin_sq_add_cos_sq
#check HasDerivAt

-- 直接用 mathlib 的定理：连续函数的复合
example (f g : ℝ → ℝ) (hf : Continuous f) (hg : Continuous g) :
    Continuous (f ∘ g) :=
  hf.comp hg

-- 三角恒等式
example (x : ℝ) : Real.sin x ^ 2 + Real.cos x ^ 2 = 1 :=
  Real.sin_sq_add_cos_sq x

-- ring 策略
example (a b : ℝ) : (a + b) ^ 2 = a ^ 2 + 2 * a * b + b ^ 2 := by
  ring

-- 导数
example (x : ℝ) : HasDerivAt (fun y : ℝ => y ^ 3) (3 * x ^ 2) x := by
  simpa using hasDerivAt_pow 3 x
