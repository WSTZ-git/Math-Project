#check Nat.add_comm
#eval 2 + 3

example (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
