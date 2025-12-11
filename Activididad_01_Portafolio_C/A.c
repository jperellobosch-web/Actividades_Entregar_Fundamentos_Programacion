#include <stdio.h> // Inclusión de la biblioteca estándar de entrada y salida (printf(), scanf()....
#include <stdlib.h> // Inclusión de la biblioteca estándar para funciones como rand() y srand(), exit()....
#include <time.h> // Inclusión de la biblioteca para funciones relacionadas con el tiempo (time())....
#include <string.h> // Inclusión de la biblioteca para funciones de manipulación de cadenas (strlen(), strcmp()....)
#include <ctype.h> // Inclusión de la biblioteca para funciones de manipulación de caracteres (tolower()....)

#define PUNTOS_INICIALES 100

/* Tirar dado 1..6 */
int tirar_dado(void) {
    return (rand() % 6) + 1; 
}

/* Leer respuesta sí/no del usuario, devuelve 1 para sí, 0 para no */
int preguntar_si_no(const char *mensaje) {
    char buf[32];
    while (1) {
        printf("%s", mensaje);
        if (!fgets(buf, sizeof(buf), stdin)) return 0;
        size_t len = strlen(buf);
        if (len && buf[len-1] == '\n') buf[len-1] = '\0';
        if (len == 0) continue;
        char c = tolower((unsigned char)buf[0]);
        if (c == 's' || c == 'y') return 1;
        if (c == 'n') return 0;
        printf("Por favor responde 's' o 'n'.\n");
    }
}

/* Turno del jugador humano */
int turno_jugador(int *puntos_jugador, int *puntos_oponente) {
    int acumulado = 0;
    printf("\n--- Turno del JUGADOR (tienes %d puntos, oponente %d puntos) ---\n", *puntos_jugador, *puntos_oponente);
    while (1) {
        int d = tirar_dado();
        printf("Tiras el dado... Ha salido: %d\n", d);
        if (d >= 2 && d <= 5) {
            acumulado += d;
            printf("Has acumulado %d puntos en este turno (acumulado = %d).\n", d, acumulado);
        } else if (d == 1) {
            printf("¡Oh no! Salió 1: pierdes el turno y se pierden los puntos acumulados.\n");
            acumulado = 0;
            return 0;
        } else { /* d == 6 */
            int op = rand() % 2; /* 0 multiplicador, 1 divisor */
            int factor = (rand() % 2) ? 3 : 2; /* 2 o 3 */
            if (op == 0) {
                acumulado = acumulado * factor;
                printf("¡Suerte! 6 -> MULTIPLICADOR x%d. Acumulado ahora = %d.\n", factor, acumulado);
            } else {
                if (factor != 0) acumulado = acumulado / factor;
                printf("6 -> DIVISOR /%d. Acumulado ahora = %d.\n", factor, acumulado);
            }
        }

        if (!preguntar_si_no("¿Quieres seguir tirando? (s/n): ")) {
            *puntos_oponente -= acumulado;
            printf("Te plantas. Se restan %d puntos al oponente. Puntos oponente = %d\n", acumulado, *puntos_oponente);
            return acumulado;
        }
    }
}

/* Turno de la máquina (CPU) */
int turno_maquina(int *puntos_maquina, int *puntos_jugador) {
    int acumulado = 0;
    const int UMBRAL = 18;
    printf("\n--- Turno de la MÁQUINA (tiene %d puntos, tú %d puntos) ---\n", *puntos_maquina, *puntos_jugador);
    while (1) {
        int d = tirar_dado();
        printf("Máquina tira... Ha salido: %d\n", d);
        if (d >= 2 && d <= 5) {
            acumulado += d;
            printf("Máquina acumula %d (acumulado máquina = %d).\n", d, acumulado);
        } else if (d == 1) {
            printf("Máquina sacó 1: pierde el turno y los puntos acumulados.\n");
            acumulado = 0;
            return 0;
        } else { /* d == 6 */
            int op = rand() % 2;
            int factor = (rand() % 2) ? 3 : 2;
            if (op == 0) {
                acumulado = acumulado * factor;
                printf("Máquina: 6 -> MULTIPLICADOR x%d. Acumulado máquina = %d.\n", factor, acumulado);
            } else {
                if (factor != 0) acumulado = acumulado / factor;
                printf("Máquina: 6 -> DIVISOR /%d. Acumulado máquina = %d.\n", factor, acumulado);
            }
        }

        if (acumulado >= UMBRAL) {
            *puntos_jugador -= acumulado;
            printf("Máquina se planta. Resta %d puntos al jugador. Tus puntos = %d\n", acumulado, *puntos_jugador);
            return acumulado;
        }

        int seguir = (rand() % 100) < 60; /* 60% probabilidad de seguir */
        if (!seguir) {
            *puntos_jugador -= acumulado;
            printf("Máquina decide plantarse. Resta %d puntos al jugador. Tus puntos = %d\n", acumulado, *puntos_jugador);
            return acumulado;
        } else {
            printf("Máquina decide seguir tirando...\n");
        }
    }
}

int main(void) {
    int puntos_jugador = PUNTOS_INICIALES;
    int puntos_maquina = PUNTOS_INICIALES;

    srand((unsigned int)time(NULL));
    printf("Juego de dados: tú contra la máquina. Ambos empezáis con %d puntos.\n", PUNTOS_INICIALES);

    while (puntos_jugador > 0 && puntos_maquina > 0) {
        turno_jugador(&puntos_jugador, &puntos_maquina);
        if (puntos_maquina <= 0) {
            printf("\n¡Has ganado! La máquina se ha quedado en %d puntos.\n", puntos_maquina);
            break;
        }

        turno_maquina(&puntos_maquina, &puntos_jugador);
        if (puntos_jugador <= 0) {
            printf("\nHas perdido. Te quedaste en %d puntos.\n", puntos_jugador);
            break;
        }

        printf("\nEstado actual: Jugador = %d, Máquina = %d\n", puntos_jugador, puntos_maquina);
    }

    printf("Fin del juego. Gracias por jugar.\n");
    return 0;
}
