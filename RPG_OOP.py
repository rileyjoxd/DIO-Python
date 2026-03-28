from abc import ABC, abstractmethod
import random
from enum import Enum

#Metade do código está em ingles porque estou acostumado a programar em inglês, o jogo assim deve estar em portugues, tirando algumas referências.

Phrases = {
"crit" : [
    f" mirou em um ponto vital.",
    f" está com sangue nos olhos.",
    f" não está para brincadeira."
],
"yowai" : [
    f" fez carinho em vez de machucar.",
    f" bateu tão fraco que ficou devendo.",
    f" tem que comer feijão."
],
"shinu" : [
    f" foi dormir em um pijama de madeira.",
    f" virou carne moída.",
    f" foi jogar no Vasco.",
    f", seja bem Vindo Ao Gigante.",
    f" virou protagonista de Isekai."
        ]        ,
}

class Character(ABC):
    def __init__(self, name, health, damage, critical, defense):
        self.name = name
        self.health = health
        self.damage = damage
        self.critical = critical
        self.defense = defense

    @abstractmethod
    def attack(self, target):
        pass
    
    def take_damage(self, amount):
        self.health -= amount
        
        if self.health <= 0: 
            self.health = 0
            print(f"{self.name}{random.choice(Phrases['shinu'])}")
            return True 
        return False
    
    def calculate_damage(self, target):
        base_damage = self.damage
        
        if hasattr(self, "weapon") and self.weapon:
            base_damage += self.weapon.damage_bonus
        
        defense = target.defense
        
        if hasattr(target, "armor") and target.armor:
            defense+= target.armor.defense_bonus
        
        damage = max(0, base_damage - defense)
        
        if self is target:
            print(f"{self.name} está atacando a sí mesmo.")
        
        total_crit = self.critical
        if hasattr(self, "weapon") and self.weapon:
            total_crit += self.weapon.crit_rate
            
        total_crit = min(total_crit, 100) #Pra não bugar o calculo, talvez adicione 4x no futuro.
            
        if random.random() < total_crit / 100:
            damage *= 2
            print(f"{self.name}{random.choice(Phrases['crit'])}")

        if damage < 0:
            print(f"{self.name}{random.choice(Phrases['yowai'])}")
        
        return damage

class NPC(Character):
    def __init__(self, name, health, damage, critical, defense, fixed_drop=None, random_drop=True):
        
        super().__init__(name, health, damage, critical, defense,)
        
        self.fixed_drop = fixed_drop or []
        self.random_drop = random_drop

    def generate_drops(self):
        loots = []

        # 🎯 1. Drops fixos (sempre acontecem)
        for generator in self.fixed_drop:
            loots.append(generator())

        # 🎲 2. Drops aleatórios (da pool global)
        if self.random_drop:
            num_drops = random.randint(1, 2)
            for _ in range(num_drops):
                loots.append(generate_loot())

        return loots

class Basic(NPC):
    def __init__(self, name, health, damage, critical, defense, fixed_drop=None, random_drop=True):
        super().__init__(name, health, damage, critical, defense, fixed_drop=fixed_drop, random_drop=random_drop)

    def attack(self, target):
        totaldmg = self.calculate_damage(target)
        died = target.take_damage(totaldmg)
        print(f"{self.name} deu {totaldmg} de dano em {target.name}.")

class Player(Character):
    def __init__(self, name, coins = 0, ):
        super().__init__(name, 100, 10, 5, 0)
        self._coins = coins #Mais inutil que buzina em avião.
        self._inventory = []
        self.weapon = None
        self.armor = None
        self.level = 1
        
        

    @property
    def coins(self):
        return self._coins
    

    def attack(self, target):
        totaldmg = self.calculate_damage(target)
        died = target.take_damage(totaldmg)
        print(f"{self.name} deu {totaldmg} de dano em {target.name}.")
        if died and isinstance(target, NPC):
            loots = target.generate_drops()

            print(f"{target.name} dropou:")

            for item in loots:
                print(f"- {item.name}")

            for item in loots:
                while True:
                    choice = input(f"Deseja pegar {item.name}? (s/n): ").lower()

                    if choice in ["s", "sim"]:
                        self.pickup_item(item)
                        break
                    elif choice in ["n", "nao", "não"]:
                        print(f"{self.name} deixou {item.name}.")
                        break
                    else:
                        print("Digite 's' ou 'n'.")


    def pickup_item(self, item):
        self._inventory.append(item)
        print(f"{self.name} pegou {item.name}")


    def drop_item(self, item):
        self._inventory.remove(item)
        print(f"{self.name} dropou {item.name}.")
        
    def use_item(self, item): #Vou deixar 2 métodos de use diferentes, hack fedorento para no caso for criar outros itens que não sejam Potions.
        if item not in self._inventory:
            print("Item não está no inventário.")
            return
        
        if isinstance(item,Potion):
            item.use(self, self) #Bem intuitivo 😂 O primeiro self é o item, o segundo é quem usou.
            self._inventory.remove(item)
        else:
            print("Esse item não pode ser bebido.")
            
    def equip_item(self, index):
        if index < 0 or index >= len(self._inventory):
            print("Indice inválido.")
            return
        
        item = self._inventory[index]
        
        if isinstance(item, Weapon):
            self.weapon = item
            print(f"{self.name} agora usa {item.name} como arma.")
            
        elif isinstance(item, Armor):
            self.armor = item
            print(f"{self.name} equipou {item.name}.")
            
        else:
            print("Esse item não pode ser equipado.")
    def show_inventory(self):
        print("Inventário:")
        
        for i, item in enumerate(self._inventory):
            equipped = ""
            
            if item == self.weapon or item == self.armor:
                equipped = " (EQUIPADO)"
                
            print(f"{i} - {item.name} ({item.rarity.name}){equipped}")
            
## Sistema de Itens

class Rarity(Enum):
    COMMON = 1
    RARE = 2
    EPIC = 3
    LEGENDARY = 4
    
def roll_rarity():
    roll = random.random()
    
    if roll < 0.6:
        return Rarity.COMMON
    elif roll < 0.85:
        return Rarity.RARE
    elif roll < 0.97:
        return Rarity.EPIC
    else:
        return Rarity.LEGENDARY

item_pool = {
    Rarity.COMMON: [
        lambda: Weapon("Palito de dente", 1, 2, Rarity.COMMON),
        lambda: Weapon("Escova de Ogro", 2, 5, Rarity.COMMON),
        lambda: Weapon("Espada de Vidro", random.randint(1,5),random.randint(1,5), Rarity.COMMON),
        lambda: Weapon("Marreta do Chapolin da Shoppee Medieval", 4, 4, Rarity.COMMON),
        lambda: Armor("Sacola de Mercado Medieval", 1, Rarity.COMMON),
        lambda: Armor("Toalha de banho", random.randint(1,2), Rarity.COMMON),
        lambda: Armor("Tronco de Árvore oco", 2, Rarity.COMMON),
        lambda: Armor("Lata de Lixo", 3, Rarity.COMMON),
        lambda: Potion("Suco de Carniça", -5, Rarity.COMMON),
        lambda: Potion("Lavagem", -2, Rarity.COMMON),
        lambda: Potion("Caldo de Cup Noodles", -1, Rarity.COMMON),
        lambda: Potion("Pão seco", random.randint(2,5), Rarity.COMMON),
        lambda: Potion("Elixir Mata-Pulga", random.randint(3,7), Rarity.COMMON),
        lambda: Potion("Chop Amanhecido", random.randint(4,7), Rarity.COMMON),
        lambda: Potion("Poção feita as coxas", random.randint(5,8), Rarity.COMMON),
        lambda: Potion("Xarope da vó de alguém", random.randint(5,9), Rarity.COMMON),
        lambda: Potion("Poção Fraca", random.randint(6,10), Rarity.COMMON)
        
    ],
    
    Rarity.RARE: [
        lambda: Weapon("Faca AK-47", 4, 10, Rarity.RARE),
        lambda: Weapon("Peixeira", 5, random.randint(5, 7), Rarity.RARE),
        lambda: Weapon("Alabarda", 9, 2, Rarity.RARE),
        lambda: Weapon("Barril de Chop", random.randint(5, 10), random.randint(5, 10), Rarity.RARE),
        lambda: Armor("Roupa de Mago", 5, Rarity.RARE),
        lambda: Armor("Armadura de Couro", 6, Rarity.RARE),
        lambda: Armor("Cota de Malha", 7, Rarity.RARE),
        lambda: Potion("PoçãoD20", random.randint(1, 20), Rarity.RARE),
        lambda: Potion("Velho Escudeiro 910ml 40%", random.randint(15,20), Rarity.RARE),
        lambda: Potion("Suco Limonations", 20, Rarity.RARE),
        lambda: Potion("Poção Mediana", random.randint(20,30), Rarity.RARE),
        lambda: Potion("Dragon Breath", random.randint(-10,40), Rarity.RARE)
    ],
    Rarity.EPIC: [
        lambda: Weapon("Night's Edge", 10, 8, Rarity.EPIC), #🌳
        lambda: Weapon("Marreta do Everson Eyes, o Bárbaro", 11, 5, Rarity.EPIC),
        lambda: Weapon("Cortador de Grama em uma vara", 12, 6, Rarity.EPIC),
        lambda: Weapon("Excalibur na Pedra", 14, 5, Rarity.EPIC),
        lambda: Armor("Armadura de Durasteel", 8, Rarity.EPIC),
        lambda: Armor("Armadura Mágica", 9, Rarity.EPIC),        
        lambda: Armor("Armadura do Sol", 10, Rarity.EPIC), #Praise the Sun 🙌
        lambda: Potion("Poção Boa", random.randint(30, 40), Rarity.EPIC),
        lambda: Potion ("Poção do Apostador", random.randint(-75, 75), Rarity.EPIC),
        lambda: Potion("Elixir da Bruxa", random.randint(40, 45), Rarity.EPIC),
        lambda: Potion("Litrão de Jester Daniels Fire", random.randint(40, 50), Rarity.EPIC),
        lambda: Potion("Leite de Burra", 50, Rarity.EPIC)    
    ],
    Rarity.LEGENDARY: [
        lambda: Weapon("Terrablade",20, 20, Rarity.LEGENDARY), #🌳
        lambda: Weapon("Dragon Slayer", 22, 10, Rarity.LEGENDARY),
        lambda: Weapon("Muramasa", 25, 12, Rarity.LEGENDARY),
        lambda: Weapon("Birch Tree", 30, 15, Rarity.LEGENDARY), #👁️
        lambda: Weapon("A Lendária Excalibur", 40, 20, Rarity.LEGENDARY),
        lambda: Weapon("Zenith", 50, 25, Rarity.LEGENDARY), #🌳
        lambda: Armor("Camiseta do Archlinux", 15, Rarity.LEGENDARY),
        lambda: Armor("Malha de Nokia", 20, Rarity.LEGENDARY),
        lambda: Armor("Camiseta de C++", 22, Rarity.LEGENDARY),
        lambda: Armor("Plot Armor", 25, Rarity.LEGENDARY),
        lambda: Armor("Camiseta de Assembly", 30, Rarity.LEGENDARY),
        lambda: Potion("Poção do Chaos", random.randint(-100, 200), Rarity.LEGENDARY),
        lambda: Potion("Poção Lendária", random.randint(50, 75), Rarity.LEGENDARY),
        lambda: Potion("PoçãoD100", random.randint(1, 100), Rarity.LEGENDARY),
        lambda: Potion("Ambrosia", 60, Rarity.LEGENDARY),
        lambda: Potion("Holy Hand Grenade Defusada", random.randint(70, 100), Rarity.LEGENDARY)
        
    ]
}
    
def generate_loot():
    rarity = roll_rarity()
    pool = item_pool[rarity]
    item_generator = random.choice(pool)
    
    return item_generator()
    

## Classes de items

class Item:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity
        
class Weapon(Item):
    def __init__(self, name, damage_bonus, crit_rate, rarity):
        super().__init__(name, rarity)
        self.damage_bonus = damage_bonus
        self.crit_rate = crit_rate

class Armor(Item):
    def __init__(self, name, defense_bonus, rarity):
        super().__init__(name, rarity)
        self.defense_bonus = defense_bonus

class Potion(Item):
    def __init__(self, name, heal, rarity):
        super().__init__(name, rarity)
        self.heal = heal
        
        
    def use(self, user, target):
        target.health += self.heal
        if user != target:
            print(f"{self.name} forçou {target.name} a beber {self.name}, seu inimigo, só pelo prazer do esporte.")
        elif self.heal >= 0:
            print(f"{user.name} bebeu {self.name}, o que lhe acrescentou {self.heal} de vida, e lhe deixou com {target.health}.")            
        else:
            print(f"{user.name} bebeu {self.name}, o que lhe tirou {-(self.heal)} de vida, e lhe deixou com {target.health} de vida, não foi a melhor idéia.")            
player = Player("Herói")
enemy = Basic(
    "Goblin Elite",
    5, 8, 5, 3,
    fixed_drop=[
        lambda: Weapon("Adaga do Goblin", 4, 3, Rarity.COMMON)
    ],
    random_drop=True
)

#Funções e companhia.

def create_enemy(player_level):
    scale = player_level
    
    health = random.randint(20 + scale*5, 30 + scale*8)
    damage = random.randint(5 + scale*2, 8 + scale*3)
    defense = random.randint(1 + scale, 3 + scale*2)
    critical = random.randint(2, 5 + scale)
    
    return Basic(
        name=random.choice(["Goblin", "Bandido", "Esqueleto"]),
        health=health,
        damage=damage,
        critical=critical,
        defense=defense
    )
'''loot = generate_loot()
player.pickup_item(loot)
player.show_inventory()
player.equip_item(0)
player.use_item(player._inventory[0])
player.attack(enemy)
player.equip_item(1)
player.equip_item(2)
player.show_inventory()''' #Código para testar os métodos, etc....

##TODO: Criar inimigos, fazer eles poderem usar itens(Não obrigatório), ajeitar a linha 353.