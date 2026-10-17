from environment import HotelEnvironment
from agent import HotelAgent
e=HotelEnvironment()
steps=HotelAgent(e).run("Rahul",2,True)
r=e.find_reservation("Rahul")
assert steps[-1]["type"]=="complete"
assert r["status"]=="checked_in" and r["room_id"] and r["late_checkout"]
print("HOTEL TEST PASSED")
