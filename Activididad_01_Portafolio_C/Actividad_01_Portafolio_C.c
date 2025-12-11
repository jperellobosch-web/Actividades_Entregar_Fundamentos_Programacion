
#include <stdio.h> // Inclusión de la biblioteca estándar de entrada y salida (printf(), scanf()....
#include <stdlib.h> // Inclusión de la biblioteca estándar para funciones como rand() y srand(), exit()....
#include <time.h> // Inclusión de la biblioteca para funciones relacionadas con el tiempo (time())....

// --- CONSTANTES ---
#define PUNTOS_INICIALES 100

// --- DEFINIMOS FUNCIONES ---
// Declaramos las funciones antes para que el main sepa que existen
int tirar_dado();
int evento_especial_6(int puntos_actuales);
int turno_jugador(int puntos_oponente);
int turno_maquina(int puntos_oponente);
void limpiar_buffer();

// --- FUNCIÓN PRINCIPAL ---
int main() {
/* Inicializar semilla para números aleatorios. La función rand() siempre genera la misma secuencia de números si no se "agita". Usamos time(NULL) como "semilla" (srand) para que, 
al arrancar el juego en distintos momentos, los dados sean distintos.*/
    srand(time(NULL)); 

    int vida_jugador = PUNTOS_INICIALES;
    int vida_maquina = PUNTOS_INICIALES;
    int danio_turno = 0; // Variable que guarda el daño infligido en cada turno del juego.

    printf("======================================\n");
    printf("     JUEGO DE DADOS: DUELO C \n");
    printf("======================================\n\n");

    // Bucle principal del juego
    while (vida_jugador > 0 && vida_maquina > 0) {
        
        // --- TURNO DEL JUGADOR ---
        printf("\n>> TU TURNO (Tu Vida: %d | Maquina: %d)\n", vida_jugador, vida_maquina); // Muestra las vidas actuales. %d viene a ser lo mismo que f{} en Python.
        danio_turno = turno_jugador(vida_maquina); // Llama a la función del turno del jugador, pasando la vida de la máquina como argumento.
        
        vida_maquina -= danio_turno; // Resta el daño infligido a la vida de la máquina.
        printf("   -> Has infligido %d puntos de daño.\n", danio_turno);

        if (vida_maquina <= 0) break; // Si la máquina muere, termina.

        // --- TURNO DE LA MÁQUINA ---
        printf("\n>> TURNO DE LA MAQUINA (Tu Vida: %d | Maquina: %d)\n", vida_jugador, vida_maquina);
        danio_turno = turno_maquina(vida_jugador);
        
        vida_jugador -= danio_turno;
        printf("   -> La maquina te ha infligido %d puntos de daño.\n", danio_turno);
    }

    // --- FIN DEL JUEGO ---
    printf("\n======================================\n");
    if (vida_maquina <= 0) {
        printf("   ¡FELICIDADES! HAS GANADO LA PARTIDA. 🏆\n");
    } else {
        printf("   GAME OVER. LA MAQUINA TE HA DERROTADO. 💀\n");
    }
    printf("======================================\n");

    return 0;
}

// --- IMPLEMENTACIÓN DE FUNCIONES ---

int tirar_dado() {
    return (rand() % 6) + 1; // Genera número entre 1 y 6. El operador % es el módulo (resto de la división). El +1 es para ajustar el rango de 0-5 (uso del ordenador) a 1-6 (uso humano).
}

// Lógica compleja del 6 (Multiplicador/Divisor y Moneda)
int evento_especial_6(int puntos_actuales) {
    printf("   ¡EVENTO ESPECIAL (6)! Tirando dados de modificador...\n");
    
    // 0 = Multiplicador, 1 = Divisor
    int es_divisor = rand() % 2; 
    
    // Genera 2 o 3. Simula la moneda.
    int factor = (rand() % 2) + 2; // +2 para ajustar el rango a 2-3. Si la máquina saca 0, 0+2=2. Si saca 1, 1+2=3.

    if (es_divisor == 0) {
        // Multiplicador
        puntos_actuales *= factor;
        printf("   ¡BONUS! Puntos acumulados se MULTIPLICAN por %d. Nuevo total: %d\n", factor, puntos_actuales);
    } else {
        // Divisor
        puntos_actuales /= factor; // División entera automática en C
        printf("   ¡MALA SUERTE! Puntos acumulados se DIVIDEN entre %d. Nuevo total: %d\n", factor, puntos_actuales);
    }
    return puntos_actuales;
}

int turno_jugador(int puntos_oponente) { // Recibe los puntos del oponente para avisar si puede ganar.
    int acumulado = 0; // Variable donde se iran acumulando los puntos en este turno.
    int dado; // Variable para almacenar el valor del dado.
    char decision; // Variable para almacenar la decisión del jugador (seguir tirando o plantarse).
    int turno_activo = 1; // 1 = verdadero, 0 = falso El turno sigue activo mientras sea 1.

    while (turno_activo) {
        printf("   [Enter para tirar dado...]");
        limpiar_buffer(); 
        /* Cuando el programa pregunta si se quiere seguir tirando el dado y se responde "S" y se pulsa "ENTER", se le está enviando dos cosas al pc, la letra y el salto de 
        línea (Enter). El comando intero del programa scanf coge la "s", pero deja el "Enter")". En la siguiente vuelta de turno, cuando el programa vuelve a preguntar para tirar el dado, si 
        no se limpia el buffer el programa ve que hay un "Enter" "flotando" del turno anterior y lo coge inmediatamente y cree que se ha pulsado otra vez y tira el dado automáticamente. Si se 
        limpia el buffer eso no ocurre, y el programa espera a que se pulse de verdad otra vez la tecla enter*/ 
        
        dado = tirar_dado();
        printf("   >>> Has sacado un: %d\n", dado);

        if (dado == 1) {
            printf("   ¡OH NO! Sacaste un 1. Pierdes el turno y los puntos acumulados.\n");
            acumulado = 0; // Pierde todo el acumulado.
            turno_activo = 0; // Rompe el bucle.
        } 
        else if (dado == 6) { // Si es el primer tiro del turno (acumulado == 0) y sale 6, vuelve a tirar hasta obtener otro resultado útil.
            if (acumulado == 0) {
                printf("   Ha salido 6 en el primer tiro; se volverá a tirar (no hay puntos aun).\n");
                do {
                    dado = tirar_dado();
                    printf("   >>> Re-tirada: %d\n", dado);
                    if (dado == 1) {
                        printf("   ¡OH NO! Re-tirada sacó 1. Pierdes el turno y los puntos acumulados.\n");
                        acumulado = 0;
                        turno_activo = 0;
                        break;
                    }
                } while (dado == 6);

                if (turno_activo) { // Si el bucle terminó y turno_activo sigue activo, procesar el nuevo dado.
                    if (dado == 6) { // Por seguridad: si sigue siendo 6, aplicar evento especial.
                        acumulado = evento_especial_6(acumulado);
                    } else if (dado >= 2 && dado <= 5) {
                        acumulado += dado;
                        printf("   Puntos acumulados en este turno: %d\n", acumulado);
                    }
                }
            } else {
                acumulado = evento_especial_6(acumulado);
            }
        } 
        else {
            acumulado += dado; // Caso 2, 3, 4, 5.
            printf("   Puntos acumulados en este turno: %d\n", acumulado);
        }

        if (turno_activo) { // Si el turno sigue activo, preguntamos si quiere plantarse.
            if (acumulado >= puntos_oponente) { // Si el acumulado es suficiente para matar al oponente, avisamos.
                printf("   ¡ATENCION! Tienes suficientes puntos para ganar (%d). ¡Plántate!\n", acumulado);
            }

            printf("   ¿Seguir tirando? (s/n): ");
            scanf(" %c", &decision); // El espacio antes de %c es vital para ignorar saltos de línea previos

            if (decision == 'n' || decision == 'N') {
                turno_activo = 0; // Se planta
            }
        }
    }
    return acumulado;
}

int turno_maquina(int puntos_oponente) {
    int acumulado = 0;
    int dado;
    int turno_activo = 1;

    // La máquina sigue tirando hasta tener 20 puntos o ganar. Ponemos un máximo de 20 puntos para evitar que se eternice.
    while (turno_activo) {
        dado = tirar_dado();
        printf("   [Maquina] tira y saca un: %d\n", dado);

        if (dado == 1) {
            printf("   [Maquina] saca un 1 y pierde todo.\n");
            acumulado = 0;
            turno_activo = 0;
        } 
        else if (dado == 6) { // Si es el primer tiro del turno (acumulado == 0) y sale 6, la máquina rerollea para obtener un resultado significativo.
            if (acumulado == 0) {
                printf("   [Maquina] salio 6 en primer tiro; vuelve a tirar.\n");
                do {
                    dado = tirar_dado();
                    printf("   [Maquina] re-tirada: %d\n", dado);
                    if (dado == 1) {
                        printf("   [Maquina] re-tirada sacó 1 y pierde el turno.\n");
                        acumulado = 0;
                        turno_activo = 0;
                        break;
                    }
                } while (dado == 6);

                if (turno_activo) {
                    if (dado == 6) {
                        acumulado = evento_especial_6(acumulado);
                    } else if (dado >= 2 && dado <= 5) {
                        acumulado += dado;
                    }
                }
            } else {
                acumulado = evento_especial_6(acumulado);
            }
        } 
        else {
            acumulado += dado;
        }

        if (turno_activo) {
            // Máquina decide si se planta
            // 1. Si ya gana con lo que tiene, se planta.
            if (acumulado >= puntos_oponente) {
                printf("   [Maquina] decide plantarse para ganar.\n");
                turno_activo = 0;
            }
            // 2. Si tiene 20 puntos o más, se planta.
            else if (acumulado >= 20) {
                printf("   [Maquina] se planta con %d puntos.\n", acumulado);
                turno_activo = 0;
            }
            // 3. Si no, sigue tirando.
            else {
                printf("   [Maquina] decide arriesgar y seguir tirando (Acumulado: %d)...\n", acumulado);
            }
        }
    }
    return acumulado;
}

void limpiar_buffer() {
    // Lee caracteres hasta encontrar un salto de línea
    int c;
    while ((c = getchar()) != '\n' && c != EOF) { }
}
/*"Función que hemos usado arriba. Es una medida de seguridad para la gestión de inputs. Como en C la función scanf no limpia el 'Enter' que pulsa el usuario, 
esta función se encarga de vaciar esa memoria intermedia para que el programa no crea erróneamente que el usuario ha vuelto a pulsar una tecla en el siguiente turno."*/ 