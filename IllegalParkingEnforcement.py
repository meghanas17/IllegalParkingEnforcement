class IllegalParkingEnforcement:
    def init(self):
        self.violation_records = {}
        self.next_incident_id = 1
        self.next_operation_id = 1
        
    def convertFileToDictionary(self):
        try:
            with open("parking_violation.txt", "r") as fileObj:
                return eval(fileObj.read())["store"]
        except FileNotFoundError:
            return []

    def insertIntoFile(self, currList):
        with open("parking_violation.txt", "w") as fileObj:
            obj = {"store": currList}
            fileObj.write(str(obj))

    def isRecordPresentInDatabase(self, id):
        currList = self.convertFileToDictionary()
        result = [-1, None]
        for index, obj in enumerate(currList):
            if obj['incident_id'] == id:
                result[0] = index
                result[1] = obj
                break
        return result 
        
    def create_violation_record(self, operation_id, incident_id, violation_type, vehicle_plate, location):
        incident_data = {
            'operation_id': operation_id,
            'incident_id': incident_id,
            'violation_type': violation_type,
            'vehicle_plate': vehicle_plate,
            'location': location
        }  
        
        currList = self.convertFileToDictionary()
        currList.append(incident_data)
        self.insertIntoFile(currList)
        print("Violation record created successfully.")  
        
    def update_violation_record(self,operation_id, incident_id, violation_type, vehicle_plate, location):
        result = self.isRecordPresentInDatabase(incident_id)
        if result[0] != -1:
            old_record = result[1]
            updated_fields = []

            if violation_type != "":
                updated_fields.append("Violation Type: " + old_record['violation_type'] + " -> " + violation_type)
                old_record['violation_type'] = violation_type

            if vehicle_plate != "":
                updated_fields.append("vehicle plate: " + old_record['vehicle_plate'] + " -> " + vehicle_plate)
                old_record['vehicle_plate'] = vehicle_plate

            if location != "":
                updated_fields.append("location: " + old_record['location'] + " -> " + location)
                old_record['location'] = location

            if updated_fields:
                print("Old Record Values:")
                for field in updated_fields:
                    print(field)
                currList = self.convertFileToDictionary()
                currList.pop(result[0])
                currList.append(old_record)
                self.insertIntoFile(currList)
                print("Violation record updated successfully.")
            else:
                print("No fields were updated. Old record values remain unchanged.")
        else:
            print("Incident ID not found.")

    def delete_violation_record(self,operation_id, incident_id):
        result = self.isRecordPresentInDatabase(incident_id)
        if result[0] != -1:
            currList = self.convertFileToDictionary()
            currList.pop(result[0])
            self.insertIntoFile(currList)
            print("Violation record deleted successfully.")
        else:
            print("Violation record not found.")

    def manage_towing_operations(self, operation_id):
        result = self.isRecordPresentInDatabase(operation_id)
        if result[0] != -1:
            currList = self.convertFileToDictionary()
            currList.pop(result[0])
            self.insertIntoFile(currList)
            print("Towing operation managed successfully.")
        else:
           print("Error: Operation ID not found.")

    def read_violation_record(self, operation_id, incident_id):
        result = self.isRecordPresentInDatabase(incident_id)
        if result[0] != -1:
            return result[1]
        else:
            print("Violation record not found.")
            return None  

    def display_violation_records(self):
        print("\nIncident Records:")
        currList = self.convertFileToDictionary()
        for data in currList:
            print("Incident ID:", data['incident_id'])
            print("Operation ID:", data['operation_id'])  # Add operation ID here
            print("Violation Type:", data['violation_type'])
            print("Vehicle Plate:", data['vehicle_plate'])
            print("location:", data['location'])
            print("\n\n")  


# Example Usage with User Input
parking_enforcement = IllegalParkingEnforcement()

while True:
    print("\n\n**")
    print("\nChoose an option:")
    print("1. Create record")
    print("2. Read record")
    print("3. Update record")
    print("4. Delete record")
    print("5. Manage towing operations")
    print("6. Exit")

    
    choice = input("Enter your choice: ")
    print("\n\n**")

    if choice == '1':
        print("\nCreating violation Record:")
        operation_id = int(input("Enter operation ID: "))
        incident_id = int(input("Enter incident ID: "))
        violation_type = input("Enter violation type: ")
        vehicle_plate = input("Enter vehicle plate: ")
        location = input("Enter Location: ")
        parking_enforcement.create_violation_record(operation_id, incident_id, violation_type, vehicle_plate, location)
    elif choice == '2':
        print("\nReading Violation Record:")
        operation_id = int(input("Enter operation ID: "))
        incident_id = int(input("Enter incident ID to read: "))
        record = parking_enforcement.read_violation_record(operation_id, incident_id)
        if record:
            print("Violation Record:")
            print("Incident ID:", incident_id)
            print("Operation ID:", operation_id)  # Add operation ID here
            print("Violation Type:", record['violation_type'])
            print("Vehicle Plate:", record['vehicle_plate'])
            print("Location:", record['location'])
    elif choice == '3':
        print("\nUpdating Violation Record:")
        operation_id = int(input("Enter operation ID: "))
        incident_id = int(input("Enter incident ID to update: "))
        result = parking_enforcement.isRecordPresentInDatabase(incident_id)
        if result[0] != -1:
            violation_type = input("Enter new violation type : ")
            vehicle_plate = input("Enter new vehicle plate : ")
            location = input("Enter new location: ")
            parking_enforcement.update_violation_record(operation_id, incident_id, violation_type, vehicle_plate, location)
        else:
            print("Incident ID not found.")
    elif choice == '4':
        print("\nDeleting Violation Record:")
        operation_id = int(input("Enter operation ID: "))
        incident_id = int(input("Enter incident ID to delete: "))
        parking_enforcement.delete_violation_record(operation_id, incident_id)
    elif choice == '5':
        print("\nManaging Towing Operations:")
        operation_id = int(input("Enter operation ID: "))
        parking_enforcement.manage_towing_operations(operation_id)
    elif choice == '6':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
