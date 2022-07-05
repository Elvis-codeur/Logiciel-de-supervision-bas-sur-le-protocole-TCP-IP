c1 = get_value("C1")
c2 = get_value("C2")
if c1 == 1:
    set_value("M1",1)
if c2 == 1:
    set_value("M1",0)

set_value("M1",1)
print("motor_value",get_value("M1"))
print("c1_value",get_value("C1"))
print("c2_value",get_value("C2"))