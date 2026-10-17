from copy import deepcopy

class HotelEnvironment:
    def __init__(self):
        self.rooms = {
            "101": {"id":"101","type":"Standard","status":"ready","guest":None},
            "102": {"id":"102","type":"Standard","status":"dirty","guest":None},
            "201": {"id":"201","type":"Deluxe","status":"ready","guest":None},
            "202": {"id":"202","type":"Deluxe","status":"occupied","guest":"Anita"},
        }
        self.reservations = [
            {"id":"RES-1001","guest_name":"Rahul","nights":2,"room_id":None,
             "late_checkout":False,"status":"reserved"},
            {"id":"RES-1002","guest_name":"Anita","nights":1,"room_id":"202",
             "late_checkout":False,"status":"checked_in"},
        ]
        self.housekeeping_tasks = []

    def find_reservation(self, guest_name):
        return next((r for r in self.reservations
                     if r["guest_name"].lower() == guest_name.lower()), None)

    def find_best_available_room(self):
        rooms = [r for r in self.rooms.values() if r["status"] in ("ready","dirty")]
        rooms.sort(key=lambda r: (r["type"] != "Deluxe", r["id"]))
        return rooms[0] if rooms else None

    def get_room(self, room_id):
        return self.rooms[room_id]

    def _reservation(self, rid):
        return next((r for r in self.reservations if r["id"] == rid), None)

    # Tools
    def create_reservation(self, guest_name, nights):
        if self.find_reservation(guest_name):
            return {"ok":False,"message":"Reservation already exists."}
        rid = f"RES-{1000+len(self.reservations)+1}"
        self.reservations.append({"id":rid,"guest_name":guest_name,"nights":nights,
                                  "room_id":None,"late_checkout":False,"status":"reserved"})
        return {"ok":True,"message":f"Created reservation {rid}."}

    def update_reservation_nights(self, reservation_id, nights):
        r = self._reservation(reservation_id)
        if not r:
            return {"ok":False,"message":"Reservation not found."}
        r["nights"] = nights
        return {"ok":True,"message":f"Reservation updated to {nights} nights."}

    def assign_room(self, reservation_id, room_id):
        r, room = self._reservation(reservation_id), self.rooms.get(room_id)
        if not r or not room:
            return {"ok":False,"message":"Reservation or room not found."}
        if room["status"] != "ready":
            return {"ok":False,"message":f"Room {room_id} is not ready."}
        r["room_id"] = room_id
        room["status"] = "reserved"
        room["guest"] = r["guest_name"]
        return {"ok":True,"message":f"Room {room_id} assigned."}

    def create_housekeeping_task(self, room_id):
        room = self.rooms.get(room_id)
        if not room or room["status"] != "dirty":
            return {"ok":False,"message":"Room is not dirty."}
        room["status"] = "cleaning"
        task_id = f"HK-{len(self.housekeeping_tasks)+1:03d}"
        self.housekeeping_tasks.append({"id":task_id,"room_id":room_id,"status":"in_progress"})
        return {"ok":True,"message":f"Housekeeping task {task_id} created."}

    def complete_housekeeping(self, room_id):
        room = self.rooms.get(room_id)
        if not room or room["status"] != "cleaning":
            return {"ok":False,"message":"Room is not being cleaned."}
        room["status"] = "ready"
        for t in self.housekeeping_tasks:
            if t["room_id"] == room_id and t["status"] == "in_progress":
                t["status"] = "completed"
        return {"ok":True,"message":f"Room {room_id} is now ready."}

    def add_late_checkout(self, reservation_id):
        r = self._reservation(reservation_id)
        if not r:
            return {"ok":False,"message":"Reservation not found."}
        r["late_checkout"] = True
        return {"ok":True,"message":"Late checkout added."}

    def check_in_guest(self, reservation_id):
        r = self._reservation(reservation_id)
        if not r or not r["room_id"]:
            return {"ok":False,"message":"Guest has no assigned room."}
        room = self.rooms[r["room_id"]]
        if room["status"] != "reserved":
            return {"ok":False,"message":"Assigned room is not ready for check-in."}
        room["status"] = "occupied"
        r["status"] = "checked_in"
        return {"ok":True,"message":f"{r['guest_name']} checked in to room {room['id']}."}

    def execute_tool(self, name, **kwargs):
        return {
            "create_reservation":self.create_reservation,
            "update_reservation_nights":self.update_reservation_nights,
            "assign_room":self.assign_room,
            "create_housekeeping_task":self.create_housekeeping_task,
            "complete_housekeeping":self.complete_housekeeping,
            "add_late_checkout":self.add_late_checkout,
            "check_in_guest":self.check_in_guest,
        }[name](**kwargs)
