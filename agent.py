class HotelAgent:
    def __init__(self, env):
        self.env = env

    def run(self, guest_name, nights, late_checkout, max_steps=20):
        goal = {"guest":guest_name,"nights":nights,"late":late_checkout}
        steps = []

        for _ in range(max_steps):
            r = self.env.find_reservation(guest_name)

            if not r:
                tool, args, summary = "create_reservation", {"guest_name":guest_name,"nights":nights}, "Create the requested reservation."
            elif r["nights"] != nights:
                tool, args, summary = "update_reservation_nights", {"reservation_id":r["id"],"nights":nights}, "Adjust the reservation to the requested number of nights."
            elif not r["room_id"]:
                room = self.env.find_best_available_room()
                if not room:
                    return steps + [{"type":"stop","summary":"No room is available."}]
                if room["status"] == "dirty":
                    # This is deliberate: observe a dirty room before assigning it.
                    tool, args, summary = "create_housekeeping_task", {"room_id":room["id"]}, f"Room {room['id']} needs housekeeping before it can be assigned."
                else:
                    tool, args, summary = "assign_room", {"reservation_id":r["id"],"room_id":room["id"]}, f"Assign ready room {room['id']}."
            else:
                room = self.env.get_room(r["room_id"])
                if room["status"] == "cleaning":
                    tool, args, summary = "complete_housekeeping", {"room_id":room["id"]}, f"Complete housekeeping for room {room['id']}."
                elif room["status"] == "reserved" and late_checkout and not r["late_checkout"]:
                    tool, args, summary = "add_late_checkout", {"reservation_id":r["id"]}, "Add the requested late checkout."
                elif r["status"] != "checked_in":
                    tool, args, summary = "check_in_guest", {"reservation_id":r["id"]}, f"Check in {guest_name}."
                else:
                    return steps + [{"type":"complete","summary":"All requested hotel conditions are satisfied."}]

            result = self.env.execute_tool(tool, **args)
            steps.append({"type":"action","tool":tool,"summary":summary,"result":result})
            if not result["ok"]:
                return steps + [{"type":"stop","summary":result["message"]}]

        return steps + [{"type":"stop","summary":"Maximum agent steps reached."}]
