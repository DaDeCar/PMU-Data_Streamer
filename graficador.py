 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import *


def anima(i):
    '''
    Graficador de una simulación en vivo de un PMU.
    
    '''
    data = generate_file('../data/PMU_live.csv')
    phase_1 = generate_phase(data, 1)
    phase_2 = generate_phase(data, 2)
    phase_3 = generate_phase(data, 3)
    
    ax1.clear()
    ax2.clear()     # Limpia el gráfico
    ax3.clear()
    
    top=0.88
    bottom=0.11
    left=0.11
    right=0.9
    hspace=0.3
    wspace=0.4
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    
    ax1.title.set_text('Senial simulada')
    ax1.plot(phase_1[0:i]['TimeStamp'], phase_1[0:i]['phase_1_signal'], label='Fase 1', color='red')
    ax1.plot(phase_2[0:i]['TimeStamp'], phase_2[0:i]['phase_2_signal'], label='Fase 2', color='blue')
    ax1.plot(phase_3[0:i]['TimeStamp'], phase_3[0:i]['phase_3_signal'], label='Fase 3', color='green')
    ax1.set_ylabel('Tension[V] (senial reconstruida)')
    ax1.legend()
    ax1.grid()
    # ax1.set_xlim(i-6, i)
    # plt.xticks(rotation=12)

    ax2.title.set_text('Representacion fasorial')
    ax2.plot(data[0:i]['TimeStamp'], data[0:i]['V1'], label='Fase 1', color='red')
    ax2.plot(data[0:i]['TimeStamp'], data[0:i]['V2'], label='Fase 2', color='blue')
    ax2.plot(data[0:i]['TimeStamp'], data[0:i]['V3'], label='Fase 3', color='green')
    ax2.set_ylabel('Amplitud[V]')
    #ax2.set_xlabel('Tiempo[S]')
    ax2.legend()
    ax2.grid()
    # ax2.set_xlim(i-6, i)
    # plt.xticks(rotation=12)

    ax3.plot(data[0:i]['TimeStamp'], data[0:i]['Phase1'], label='Fase 1', color='red')
    ax3.plot(data[0:i]['TimeStamp'], data[0:i]['Phase2'], label='Fase 2', color='blue')
    ax3.plot(data[0:i]['TimeStamp'], data[0:i]['Phase3'], label='Fase 3', color='green')
    ax3.set_ylabel('Fase[°]')
    ax3.set_xlabel('Tiempo[S]')
    ax3.legend()
    ax3.grid()
    ax3.set_xlim(i-6, i)
    plt.xticks(rotation=12)
    
    #formato de ejes x en graficos 1 y 2
    ax1.get_shared_x_axes().join(ax1, ax2)
    ax1.set_xticklabels([])
    ax1.get_shared_x_axes().join(ax2, ax3)
    ax2.set_xticklabels([])


if __name__ == '__main__':
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle('Senial trifasica aleatoria', fontsize=12)
    anim = animation.FuncAnimation(fig, func=anima, interval=500)
    #anim.save('basic_animation.mp4', fps=10, extra_args=['-vcodec', 'libx264'])
    plt.show()



