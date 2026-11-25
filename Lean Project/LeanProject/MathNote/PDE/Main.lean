namespace LeanProject.Paper.UndergraduateThesis

/-- 测试：simp 可用 -/
example (n : Nat) : n + 0 = n := by simp

end LeanProject.Paper.UndergraduateThesis

def mul (n : Nat)(m : Nat) : Nat := n * m

#check mul

