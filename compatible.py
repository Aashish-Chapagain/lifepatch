compatible_donors = {
    "O-": ["O-"],
    "O+": ["O+", "O-"],
    "A-": ["A-", "O-"],
    "A+": ["A+", "A-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "AB-": ["AB-", "A-", "B-", "O-"],
    "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]  
}



bolood_type_list = ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"]

while True:

 user_blood_type = input("Enter your blood type (e.g., O-, A+, B+): ").strip().upper()
 if user_blood_type not in bolood_type_list :
   print("Invalid blood type. Please enter a valid blood type (e.g., O-, A+, B+).")
   continue
 else : 
   matching_donors = compatible_donors.get(user_blood_type, [])
   print("Compatible blood donors for your type ({}) are: {}".format(user_blood_type, ", ".join(matching_donors)))
   break
 





