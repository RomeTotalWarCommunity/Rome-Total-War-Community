from tkinter import filedialog

class Unit:
    def __init__(self, prec, p_attack, s_attack, p_charge, s_charge, is_missile, missile_range, is_armour_piercing, is_body_piercing,
                 is_area, is_body_launching, armour, defense, shield, morale, category, mount, mount_attack, mount_charge, mount_is_area,
                 mount_is_launch, mount_is_ap, mount_armour, hp, mount_hp, soldiers, officers, extras, name):
        self.prec = prec
        self.p_attack = p_attack
        self.s_attack = s_attack
        self.p_charge = p_charge
        self.s_charge = s_charge
        self.is_missile = is_missile
        self.missile_range = missile_range
        self.is_armour_piercing = is_armour_piercing
        self.is_body_piercing = is_body_piercing
        self.is_area = is_area
        self.is_body_launching = is_body_launching
        self.armour = armour
        self.defense = defense
        self.shield = shield
        self.morale = morale
        self.category = category
        self.mount = mount
        self.mount_attack = mount_attack
        self.mount_charge = mount_charge
        self.mount_is_area = mount_is_area
        self.mount_is_launch = mount_is_launch
        self.mount_is_ap = mount_is_ap
        self.mount_armour = mount_armour
        self.hp = hp
        self.mount_hp = mount_hp
        self.soldiers = soldiers
        self.officers = officers
        self.extras = extras
        self.name = name
        
    def get_name(self):
        return self.name
    
    def get_value(self):
        value = 0
        extra = 0
        morale_influence = 1
        
        if self.prec:
            value += self.s_attack + 2 + 0.5 * self.s_charge
        elif self.is_missile:
            value += 0.5 * self.p_attack
            morale_influence = 0.8
            if self.missile_range > 200:
                value += 4
            else:
                value += 0.02 * self.missile_range
        else:
            value += self.p_attack + 0.5 * self.p_charge
            
        value += self.armour * 4 + self.defense * 2 + self.shield * 2
        
        mor = self.morale
        if mor > 12:
            mor = 12
        elif mor < 0:
            mor = 0
        morfac = 0.25 + (0.55 * (mor * 0.0833))
        morfac = 1 - ((1 - morfac) * morale_influence)
        if self.category == "cavalry":
            if self.mount == "horse":
                value += 4
            if self.mount == "chariot":
                value += 5
            elif self.mount == "elephant":
                extra = self.mount_attack + 0.5 * self.mount_charge
                if self.mount_is_ap:
                    extra += 5
                if self.mount_is_launch:
                    extra += 1
                if self.mount_is_area:
                    extra *= 2
                    
                extra += self.mount_armour
                extra *= self.mount_hp * self.extras
                extra *= morfac
        elif self.category == "siege":
            range_mul = 0
            if self.missile_range > 210:
                range_mul = 3
            else:
                range_mul = self.missile_range * 0.01429
            mis_pow = 1.5 * self.s_attack
            extra += mis_pow + (mis_pow * range_mul)
            
            if self.is_armour_piercing:
                extra += 3
            if self.is_body_launching:
                extra += 3
            if self.is_area:
                extra *= 2.5
            elif self.is_body_piercing:
                extra *= 1.4
            extra *= self.extras
            extra *= morfac
            if self.armour < 4:
                value += 3
        elif self.category == "handler":
            extra += self.s_attack + self.mount_armour
            extra *= self.mount_hp * self.extras
            
        value *= morfac
        value *= (self.soldiers * self.hp) + (self.officers * (self.hp + 1))

        return (value + extra) * 0.45


def startswith_s_t_n(line):
    if line.startswith(' ') or line.startswith('\n') or line.startswith('\t') or line.startswith(';'):
        return True
    return False

def find_line(lines, start):
    for line in lines:
        if line.startswith(start):
            return line
    return ""

def remove_start(line, start):
    res = line.replace(start, "", 1)
    while startswith_s_t_n(res):
        if res.startswith('\n') or res.startswith(';'):
            return ""
        elif res.startswith('\t') or res.startswith(' '):
            res = res[1:]
    return res
        
edu = filedialog.askopenfilename()
edu = open(edu, 'r')

output = filedialog.askopenfilename()
output = open(output, 'w')

lines = edu.readlines()
    
edu.close()

for i in range(len(lines) - 1, -1, -1):
    while startswith_s_t_n(lines[i]):
        if lines[i].startswith('\n') or lines[i].startswith(';'):
            lines.pop(i)
            break
        elif lines[i].startswith('\t') or lines[i].startswith(' '):
            lines[i] = lines[i][1:]

for i in range(len(lines)):
    if ';' in lines[i]:
        lines[i] = lines[i].split(';')[0]

unit_list = []
line = 0
while line < len(lines):
    unit = [lines[line]]
    line += 1
    while line < len(lines) and not lines[line].startswith("type"):
        unit.append(lines[line])
        line += 1
        
    unit_list.append(unit)
        
if not lines[0].startswith("type"):
    unit_list.pop(0)
    
units = []
for lines in unit_list:
    name = find_line(lines, "dictionary").replace("dictionary", "", 1).replace("\t", "").replace(" ", "").replace("\n", "")
    prec = False
    if "prec" in find_line(lines, "stat_pri_attr"):
        prec = True
    stat_pri = remove_start(find_line(lines, "stat_pri"), "stat_pri").split(", ")
    p_attack = int(stat_pri[0])
    p_charge = int(stat_pri[1])
    missile_range = int(stat_pri[3])
    stat_sec = remove_start(find_line(lines, "stat_sec"), "stat_sec").split(", ")
    s_attack = int(stat_sec[0])
    s_charge = int(stat_sec[1])
    is_missile = False
    if "missile" in find_line(lines, "class"):
        is_missile = True
    is_armour_piercing = False
    if "ap" in find_line(lines, "stat_sec_attr"):
        is_armour_piercing = True
    is_body_piercing = False
    if "bp" in find_line(lines, "stat_sec_attr"):
        is_body_piercing = True
    is_area = False
    if "area" in find_line(lines, "stat_sec_attr"):
        is_area = True
    is_body_launching = False
    if "launching" in find_line(lines, "stat_sec_attr"):
        is_body_launching = True
    
    stat_pri_armour = remove_start(find_line(lines, "stat_pri_armour"), "stat_pri_armour").split(", ")
    armour = int(stat_pri_armour[0])
    defense = int(stat_pri_armour[1])
    shield = int(stat_pri_armour[2])

    morale = int(remove_start(find_line(lines, "stat_mental"), "stat_mental").split(", ")[0])
    category = remove_start(find_line(lines, "category"), "category")

    mount = ''
    if "horse" in find_line(lines, "mount"):
        mount = "horse"
    if "chariot" in find_line(lines, "mount"):
        mount = "chariot"
    if "elephant" in find_line(lines, "mount"):
        mount = "elephant"

    mount_attack = s_attack
    mount_charge = s_charge
    mount_is_area = is_area
    mount_is_launch = is_body_launching
    mount_is_ap = is_armour_piercing
    mount_armour = remove_start(find_line(lines, "stat_sec_armour"), "stat_sec_armour").split(", ")[0]

    health = remove_start(find_line(lines, "stat_health"), "stat_health").split(", ")
    hp = int(health[0])
    mount_hp = int(health[1])
    
    soldier = remove_start(find_line(lines, "soldier"), "soldier").split(", ")
    soldiers = int(soldier[1])
    extras = int(soldier[2])
    
    officers = 0
    for line in lines:
        if line.startswith("officer"):
            officers += 1
    
    units.append(Unit(prec, p_attack, s_attack, p_charge, s_charge, is_missile, missile_range, is_armour_piercing, is_body_piercing, is_area, 
                      is_body_launching, armour, defense, shield, morale, category, mount, mount_attack, mount_charge, mount_is_area, 
                      mount_is_launch, mount_is_ap, mount_armour, hp, mount_hp, soldiers, officers, extras, name))

print("unit,value", file = output)
for unit in units:
    uvalue = unit.get_value()
    print(unit.get_name() + ',' + str(unit.get_value()), file = output)
    
output.close()
    
    