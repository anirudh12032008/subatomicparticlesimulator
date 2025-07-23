# Super Cool Particle Collision Thing!
# This is like when tiny things crash into each other really fast

# All the particles we know about
particles = {
    "electron": {"mass": 0.5, "charge": -1, "name": "electron"},
    "positron": {"mass": 0.5, "charge": 1, "name": "positron"},
    "proton": {"mass": 938, "charge": 1, "name": "proton"},
    "neutron": {"mass": 940, "charge": 0, "name": "neutron"},
    "photon": {"mass": 0, "charge": 0, "name": "photon"},
    "muon": {"mass": 106, "charge": -1, "name": "muon"},
    "pion": {"mass": 140, "charge": 0, "name": "pion"}
}

def show_particles():
    """Show all the particles we can crash together"""
    print("\nHere are all the particles you can pick:")
    for name, data in particles.items():
        print(f"- {name}: mass = {data['mass']} MeV, charge = {data['charge']}")

def pick_particle():
    """Let the user pick a particle"""
    # Show the list with numbers
    particle_list = list(particles.keys())
    print("\nAvailable particles:")
    for i, name in enumerate(particle_list, 1):
        data = particles[name]
        print(f"{i}. {name} (mass: {data['mass']} MeV, charge: {data['charge']})")
    
    while True:
        choice = input("\nPick a particle (name or number): ").strip()
        
        # Try number first
        try:
            num = int(choice)
            if 1 <= num <= len(particle_list):
                name = particle_list[num - 1]
                return name, particles[name]
            else:
                print(f"Pick a number between 1 and {len(particle_list)}!")
                continue
        except ValueError:
            pass
        
        # Try name
        name = choice.lower()
        if name in particles:
            return name, particles[name]
        
        print("Hmm, I don't know that one. Try again!")

def get_energy():
    """Get how much energy the particle has"""
    print("\nEnergy guide (all in MeV):")
    print("- Low energy (1-10): Like a gentle push")
    print("- Medium energy (50-200): Like a baseball throw") 
    print("- High energy (500-1000): Like a rocket launch")
    print("- Super high (1000+): Like lightning!")
    print("\nFor comparison:")
    print("- Chemical reactions: ~1-10 MeV")
    print("- Nuclear reactions: ~100-1000 MeV")
    print("- Particle accelerators: 1000+ MeV")
    
    while True:
        try:
            energy = float(input("\nHow much energy does it have? (in MeV) "))
            if energy > 0:
                return energy
            print("Energy has to be more than zero!")
        except ValueError:
            print("That's not a number! Try again.")

def check_charge_ok(p1, p2, result_particles):
    """Make sure charge doesn't disappear"""
    start_charge = p1["charge"] + p2["charge"]
    end_charge = sum(particles[p]["charge"] for p in result_particles)
    return start_charge == end_charge

def figure_out_collision(p1_name, p1_data, e1, p2_name, p2_data, e2):
    """Figure out what happens when particles crash"""
    total_energy = e1 + e2
    
    # Special case: electron + positron = they destroy each other!
    if (p1_name == "electron" and p2_name == "positron") or (p1_name == "positron" and p2_name == "electron"):
        if total_energy > 1:  # Need enough energy
            return ["photon", "photon"], "Boom! They destroyed each other and made light!"
    
    # Photon crashes
    if p1_name == "photon" or p2_name == "photon":
        if total_energy > 200:
            return ["electron", "positron"], "The light made new particles!"
        else:
            return [p1_name, p2_name], "The light just bounced off."
    
    # Really high energy crashes
    if total_energy > 1000:
        if p1_data["charge"] != 0 and p2_data["charge"] != 0:
            return ["proton", "neutron", "pion"], "Huge crash! Made lots of new stuff!"
    
    # Medium energy crashes
    if total_energy > 500:
        return ["muon", "pion"], "Made some medium-heavy particles!"
    
    # Small crashes - they just bounce
    if total_energy > 50:
        return [p1_name, p2_name], "They bounced off each other like rubber balls!"
    
    # Very gentle bumps
    return [p1_name, p2_name], "They barely touched and kept going."

def do_collision():
    """Make two particles crash into each other"""
    print("\n=== Time for a particle crash! ===")
    
    # Pick first particle
    print("\nFirst particle:")
    p1_name, p1_data = pick_particle()
    e1 = get_energy()
    
    # Pick second particle
    print("\nSecond particle:")
    p2_name, p2_data = pick_particle()
    e2 = get_energy()
    
    # Show what we're crashing
    print(f"\nOkay! Crashing {p1_name} (energy: {e1}) into {p2_name} (energy: {e2})...")
    print("CRASH!")
    
    # Figure out what happens
    result, story = figure_out_collision(p1_name, p1_data, e1, p2_name, p2_data, e2)
    
    # Show the result
    print(f"\nWhat happened: {story}")
    print("After the crash, we found:")
    for particle in result:
        if particle in particles:
            data = particles[particle]
            print(f"- {particle} (mass: {data['mass']}, charge: {data['charge']})")
    
    # Check if charge is okay
    if check_charge_ok(p1_data, p2_data, result):
        print("Charge conservation: All good!")
    else:
        print("Charge conservation: Something weird happened...")

def look_at_particle():
    """Look at one particle really close"""
    print("\n=== Particle Detective Mode ===")
    name, data = pick_particle()
    
    print(f"\nLooking at {name} under our super microscope...")
    print(f"Mass: {data['mass']} MeV (that's how heavy it is)")
    print(f"Charge: {data['charge']} (positive, negative, or neutral)")
    
    # Fun facts about each particle
    facts = {
        "electron": "This little guy makes electricity work!",
        "positron": "This is like an electron but backwards!",
        "proton": "This lives in the middle of atoms.",
        "neutron": "This also lives in atoms but has no charge.",
        "photon": "This is pure light! It has no weight at all.",
        "muon": "This is like a heavy electron that doesn't last long.",
        "pion": "This helps hold the atom's center together."
    }
    
    if name in facts:
        print(f"Cool fact: {facts[name]}")

def main_menu():
    """The main menu where you pick what to do"""
    while True:
        print("\n" + "="*40)
        print("Welcome to the Particle Collision Lab!")
        print("="*40)
        print("What do you want to do?")
        print("1. Crash two particles together")
        print("2. Look at all the particles")
        print("3. Examine one particle closely")
        print("4. Quit")
        
        choice = input("\nPick a number: ").strip()
        
        if choice == "1":
            do_collision()
        elif choice == "2":
            show_particles()
        elif choice == "3":
            look_at_particle()
        elif choice == "4":
            print("\nThanks for playing with particles! Bye!")
            break
        else:
            print("That's not a choice! Pick 1, 2, 3, or 4.")

# Start the program!
if __name__ == "__main__":
    main_menu()
