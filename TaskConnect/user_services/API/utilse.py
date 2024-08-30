from ..models import *
from faker import Faker
import random
from django.contrib.auth.hashers import make_password


def run_faker():
    faker = Faker()
    import pdb; pdb.set_trace()
    addresses = Address.objects.all()
    organizations = Organization.objects.all()
    roles = Role.objects.all()

    for _ in range(4):  # Generate 10 dummy users
        user = User(
        name=faker.name(),
        phone=faker.phone_number()[:12].strip(),  # Trim phone number to match your max_length
        gender=random.choice(['M', 'F']),
        address=random.choice(addresses) if addresses.exists() else None,
        location=f"{faker.latitude()}, {faker.longitude()}",
        email=faker.unique.email(),
        # user_type=random.choice(['Customer', 'ServiceProvider']),
        user_type="ServiceProvider",
        # work_status=random.choice(['REQUESTED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']),
        # organization=random.choice(organizations) if organizations.exists() else None,
        password = make_password("password@123")
        )    
        user.save()
    # Add some roles to the user
    if roles.exists():
        user.user_role.set(random.sample(list(roles), random.randint(0, 3)))  # Assign 0 to 3 roles
    user.save()
    print("User saved")
    return True






roles_with_descriptions = [
    {"role": "Electrician", "description": "Installs and repairs electrical systems and wiring."},
    {"role": "Plumber", "description": "Specializes in installing and repairing water supply and drainage systems."},
    {"role": "Carpenter", "description": "Builds and repairs wooden structures and furniture."},
    {"role": "Painter", "description": "Applies paint and finishes to buildings and other structures."},
    {"role": "Cleaner", "description": "Provides cleaning services for homes, offices, and other spaces."},
    {"role": "Handyman", "description": "Performs general maintenance and repair tasks around homes and businesses."},
    {"role": "Gardener", "description": "Takes care of gardens, plants, and lawns."},
    {"role": "HVAC Technician", "description": "Installs and maintains heating, ventilation, and air conditioning systems."},
    {"role": "Mechanic", "description": "Repairs and maintains vehicles and machinery."},
    {"role": "Pest Control Specialist", "description": "Handles the removal and prevention of pests and vermin."},
    {"role": "Mason", "description": "Works with stone, brick, and concrete to build structures."},
    {"role": "Landscaper", "description": "Designs and maintains outdoor landscapes and gardens."},
    {"role": "Locksmith", "description": "Installs and repairs locks and security systems."},
    {"role": "Roofer", "description": "Installs and repairs roofs on buildings."},
    {"role": "Welder", "description": "Joins metal parts using heat and pressure."},
    {"role": "Home Appliance Repairer", "description": "Fixes and maintains household appliances."},
    {"role": "IT Support Specialist", "description": "Provides technical support for computer systems and networks."},
    {"role": "Moving & Relocation Specialist", "description": "Assists with packing, moving, and setting up in new locations."},
    {"role": "Tailor/Seamstress", "description": "Alters and repairs clothing and other textiles."},
    {"role": "Laundry Services", "description": "Provides washing, drying, and ironing services for clothes and linens."}
]

def set_roles():
    for item in roles_with_descriptions:
        Role.objects.create(role_name = item['role'], description = item['description'])
    print("done")

dummy_addresses = [
    {
        "street": "123 Elm St",
        "city": "Springfield",
        "state": "IL",
        "postal_code": "62704",
        "country": "USA",
    },
    {
        "street": "456 Oak Ave",
        "city": "Greenville",
        "state": "SC",
        "postal_code": "29601",
        "country": "USA",
    },
    {
        "street": "789 Maple Rd",
        "city": "Fairview",
        "state": "TX",
        "postal_code": "75069",
        "country": "USA",
    },
    {
        "street": "101 Pine Blvd",
        "city": "Riverside",
        "state": "CA",
        "postal_code": "92501",
        "country": "USA",
    },
    {
        "street": "202 Cedar St",
        "city": "Lakeview",
        "state": "FL",
        "postal_code": "32055",
        "country": "USA",
    },
]

    
def set_address():
    for item in dummy_addresses:
        Address.objects.create(
            street = item['street'], 
            city = item['city'],
            state = item['state'], 
            postal_code = item['postal_code'],
            country = item['country']
        )
    print("done")

dummy_organizations = [
    {
        "name": "Tech Solutions Inc.",
        "address": 1,  # Assuming 1 is the primary key (id) of the first Address instance
        "contact_email": "contact@techsolutions.com",
        "phone": "+1-800-555-1234",
    },
    {
        "name": "Green Earth Services",
        "address": 2,  # Assuming 2 is the primary key (id) of the second Address instance
        "contact_email": "info@greenearth.com",
        "phone": "+1-800-555-5678",
    },
    {
        "name": "Innovative Designs",
        "address": 3,  # Assuming 3 is the primary key (id) of the third Address instance
        "contact_email": "hello@innovativedesigns.com",
        "phone": "+1-800-555-9012",
    },
    {
        "name": "Global Logistics Ltd.",
        "address": 4,  # Assuming 4 is the primary key (id) of the fourth Address instance
        "contact_email": "support@globallogistics.com",
        "phone": "+1-800-555-3456",
    },
    {
        "name": "Healthcare Partners",
        "address": 5,  # Assuming 5 is the primary key (id) of the fifth Address instance
        "contact_email": "contact@healthpartners.com",
        "phone": "+1-800-555-7890",
    },
]
def set_organization():
    for item in dummy_organizations:
        Organization.objects.create(
            name = item['name'],
            contact_email = item['contact_email'], 
            phone = item['phone']
        )
    print("done")

