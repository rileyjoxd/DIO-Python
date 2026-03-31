from RPG_OOP import *

#Quem não tem API caça com Terminal.

def show_status(player, enemy):
    print(f"\n{'='*40}")
    print(f"  {player.name} | HP: {player.health} | Nível: {player.level}")
    arma = player.weapon.name if player.weapon else "Nenhuma"
    armadura = player.armor.name if player.armor else "Nenhuma"
    print(f"  Arma: {arma} | Armadura: {armadura}")
    print(f"  {'-'*38}")
    print(f"  {enemy.name} | HP: {enemy.health}")
    print(f"{'='*40}\n")
    
def menu_inventario(player):
    while True:
        print("\n--- INVENTÁRIO ---")
        if not player._inventory:
            print("  Inventário vazio.")
            return
        
        player.show_inventory()
        print("\nO que deseja fazer?")
        print("  1 - Usar item (poção)")
        print("  2 - Equipar item")
        print("  3 - Voltar")
        
        acao = input("> ").strip()
        
        if acao == "1":
            idx = input("Índice do item para usar: ").strip()
            if idx.isdigit():
                idx = int(idx)
                if 0 <= idx < len(player._inventory):
                    player.use_item(player._inventory[idx])
                else:
                    print("Índice inválido.")
                return
        
        elif acao == "2":
            idx = input("Escolha o índice do item para equipar: ").strip()
            if idx.isdigit():
                player.equip_item(int(idx))
        
        elif acao == "3":
            return
        else:
            print("Opção inválida.")
            
def combat_loop(player, enemy):
    print(f"\nUm {enemy.name} apareceu!\n")
    
    while player.health > 0 and enemy.health > 0: #loop meio hack, substituir no futuro.
        show_status(player, enemy)
        
        print("O que deseja fazer?")
        print("  1 - Atacar")
        print("  2 - Inventário")
        print("  3 - Fugir")

        acao = input("> ").strip()
    
        if acao == "1":
            player.attack(enemy)
            if enemy.health <= 0:
                print(f"\nVocê derrotou {enemy.name}!")
                player.level += 1 #Sistema de level será retrabalhado no futuro, por enquanto todos os inimigos dão 1 level.
                print(f"Subiu para o nível {player.level}!")
                return True  # Vitória
            
            print(f"\n{enemy.name} contra-ataca!")
            enemy.attack(player)
            
            if player.health <= 0:
                print("\nVocê foi derrotado... Game Over.")
                return False #Derrota
            
        elif acao == "2":
            menu_inventario(player)
            
        elif acao == "3":
            chance_fuga = 0.4
            if random.random() < chance_fuga:
                print("Você fugiu com sucesso!")
                return None  # Fuga
            else:
                print("Não conseguiu fugir!")
                enemy.attack(player)
                if player.health <= 0:
                    print("\nVocê foi derrotado... Game Over.")
                    return False
                
        else:
            print("Opção inválida.")
            
    return player.health > 0

def evento_bau(player):
    if random.random() < 0.3:
        Chest(player)
        
def game_loop():
    nome = input("Digite o nome do seu personagem: ").strip() or "Hérói"
    player = Player(nome)
    
    print(f"\nBem-vindo, {player.name}! Sua aventura começa agora.")
    batalhas = 0
    
    while player.health > 0:
        input("\n[Pressione Enter para continuar...]\n")
        
        enemy = create_enemy(player.level)
        resultado = combat_loop(player, enemy)
        
        if resultado is False: #Faleceu
            break
        elif resultado is True: #Venceu
            batalhas += 1
            evento_bau(player)
        #Se der None, como no fugiu, o loop procede normalmente.
        
    print(f"\n--- FIM DE JOGO ---")
    print(f"  Personagem> {player.name}")
    print(f"  Nível alcançado: {player.level}")
    print(f"  Batalhas vencidas: {batalhas}")
    
if __name__ == "__main__": #Proteção pro código não rodar se for importado.
    game_loop()