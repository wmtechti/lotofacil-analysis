"""
Utilidades comuns para análise de apostas da Lotofácil.
"""

def determinar_nivel_premiacao(num_acertos):
    """
    Determina o nível de premiação baseado no número de acertos.
    
    Args:
        num_acertos: Número de acertos (0-15)
        
    Returns:
        String com emoji e descrição do nível de premiação
    """
    if num_acertos == 15:
        return "🎯 QUINZE PONTOS!"
    elif num_acertos == 14:
        return "⭐ QUATORZE PONTOS!"
    elif num_acertos == 13:
        return "✨ TREZE PONTOS!"
    elif num_acertos == 12:
        return "🌟 DOZE PONTOS!"
    elif num_acertos == 11:
        return "💫 ONZE PONTOS!"
    else:
        return f"❌ Não premiado"
