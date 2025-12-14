"""
Aplicación principal con interfaz de línea de comandos (CLI).
"""

import logging
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import CustomerServiceAgent
from src.config import LOG_LEVEL

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("customer_service.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def print_banner():
    """Imprime el banner de bienvenida."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        🏦  BANCO HENRY - Sistema de Atención             ║
║                  al Cliente Automatizado                  ║
║                                                           ║
║        Powered by LangChain & OpenAI GPT-4               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def print_help():
    """Imprime el menú de ayuda."""
    help_text = """
📋 COMANDOS DISPONIBLES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Consultas que puedes hacer:

  1️⃣  Consulta de Balance:
     • "¿Cuál es el balance de la cédula V-12345678?"
     • "Consultar saldo de mi cuenta"
     • "Balance V-91827364"

  2️⃣  Información Bancaria:
     • "¿Cómo abrir una cuenta de ahorros?"
     • "¿Cómo solicitar una tarjeta de crédito?"
     • "¿Cómo hacer una transferencia?"
     • "Requisitos para abrir cuenta"

  3️⃣  Preguntas Generales:
     • "¿Qué servicios ofrecen?"
     • "Horarios de atención"
     • Cualquier otra pregunta

🔧 Comandos del Sistema:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  /help     - Muestra este menú de ayuda
  /stats    - Muestra estadísticas de uso
  /clear    - Limpia la pantalla
  /exit     - Salir del sistema
  /quit     - Salir del sistema

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(help_text)


def print_stats(agent: CustomerServiceAgent):
    """Imprime estadísticas del sistema."""
    stats = agent.get_statistics()

    stats_text = f"""
📊 ESTADÍSTICAS DEL SISTEMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total de consultas procesadas: {stats['total_queries']}

Desglose por tipo:
  💰 Consultas de balance:        {stats['balance_queries']}
  📚 Consultas de base de conocimiento: {stats['knowledge_queries']}
  💬 Consultas generales:         {stats['general_queries']}

Tasa de éxito: {stats['success_rate']:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(stats_text)


def clear_screen():
    """Limpia la pantalla."""
    import os

    os.system("cls" if os.name == "nt" else "clear")


def format_response(result: dict) -> str:
    """Formatea la respuesta para mejor visualización."""
    emoji_map = {"balance": "💰", "knowledge": "📚", "general": "💬", "error": "❌"}

    query_type = result.get("query_type", "general")
    emoji = emoji_map.get(query_type, "💬")

    output = f"\n{emoji} Tipo de consulta: {query_type.upper()}\n"
    output += "━" * 60 + "\n\n"
    output += result["response"]
    output += "\n\n" + "━" * 60 + "\n"

    return output


def interactive_mode():
    """Modo interactivo de la aplicación."""
    clear_screen()
    print_banner()

    print("\n🔄 Inicializando el sistema...")
    print("⏳ Esto puede tardar unos segundos...\n")

    try:
        agent = CustomerServiceAgent()
        print("✅ Sistema inicializado correctamente!\n")
        print_help()

        while True:
            try:
                # Solicitar input del usuario
                user_input = input("\n🙋 Tu consulta (o /help para ayuda): ").strip()

                if not user_input:
                    continue

                # Procesar comandos del sistema
                if user_input.startswith("/"):
                    command = user_input.lower()

                    if command in ["/exit", "/quit"]:
                        print("\n👋 ¡Gracias por usar BANCO HENRY! Hasta pronto.\n")
                        break
                    elif command == "/help":
                        print_help()
                        continue
                    elif command == "/stats":
                        print_stats(agent)
                        continue
                    elif command == "/clear":
                        clear_screen()
                        print_banner()
                        continue
                    else:
                        print(f"❌ Comando desconocido: {command}")
                        print("💡 Usa /help para ver los comandos disponibles")
                        continue

                # Procesar consulta
                print("\n🤔 Procesando tu consulta...\n")
                result = agent.process_query(user_input)

                # Mostrar respuesta
                print(format_response(result))

            except KeyboardInterrupt:
                print("\n\n👋 Saliendo del sistema...")
                break
            except Exception as e:
                logger.error(f"Error en modo interactivo: {e}", exc_info=True)
                print(f"\n❌ Error: {e}\n")

    except Exception as e:
        logger.error(f"Error al inicializar el sistema: {e}", exc_info=True)
        print(f"\n❌ Error fatal al inicializar: {e}")
        print("💡 Verifica que tu archivo .env esté configurado correctamente")
        sys.exit(1)


def batch_mode(queries: list):
    """
    Modo batch para procesar múltiples consultas.

    Args:
        queries: Lista de consultas a procesar
    """
    print("🔄 Modo batch activado")
    print(f"📝 Procesando {len(queries)} consultas...\n")

    agent = CustomerServiceAgent()
    results = []

    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] Procesando: {query}")
        result = agent.process_query(query)
        results.append({"query": query, "result": result})
        print(format_response(result))

    print("\n✅ Procesamiento batch completado")
    print_stats(agent)

    return results


def main():
    """Función principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sistema de Atención al Cliente Automatizado - BANCO HENRY"
    )
    parser.add_argument("--query", "-q", type=str, help="Consulta única a procesar")
    parser.add_argument(
        "--batch", "-b", type=str, help="Archivo con consultas (una por línea)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Modo verbose (más logs)"
    )

    args = parser.parse_args()

    # Ajustar nivel de logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Modo consulta única
    if args.query:
        agent = CustomerServiceAgent()
        result = agent.process_query(args.query)
        print(format_response(result))
        return

    # Modo batch
    if args.batch:
        try:
            with open(args.batch, "r", encoding="utf-8") as f:
                queries = [line.strip() for line in f if line.strip()]
            batch_mode(queries)
        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {args.batch}")
            sys.exit(1)
        return

    # Modo interactivo (default)
    interactive_mode()


if __name__ == "__main__":
    main()
