import numpy as np
import math 
import pandas as pd
from datetime import datetime, timezone

class SineWave:
    """
    Representa una señal senoidal monofasica con la posibilidad de sumarle ruido aleatorio.
    Las magnitudes de ruido deben ingresarse en porcentajes (x ej:5, 0.2, 2 ),
    lo que viene a ser el 5%, 0.2% y 2% de ruido respectivamente
    """
    def __init__(self, frequency, amplitude, phase,freq_noise,amp_noise,phase_noise,
                 frames_p_sec) -> None:
        self.frequency = frequency  
        self.amplitude = amplitude  
        self.phase = phase  
        self.w = 2*np.pi*frequency      # angular frequency
  
        # Ruido (en %)
        self.amp_noise=amp_noise
        self.freq_noise=freq_noise
        self.phase_noise = phase_noise         
        
        # Determinación de max y min de magnitudes de la señal
        amplitude_min, amplitude_max = self.amplitude*(1-self.amp_noise /100), self.amplitude*(1+self.amp_noise /100) 
        phase_min, phase_max = self.phase*(1-self.phase_noise/100), self.phase*(1+self.phase_noise/100) 
        freq_min, freq_max = self.frequency*(1-self.freq_noise/100), self.frequency*(1+self.freq_noise/100)
        
        # Construccion de vectores de la señal
        self.fps=frames_p_sec
        # array de fase de fasor
        self.phasors_phase = np.random.uniform(low=phase_min, high=phase_max, size=self.fps)
        # array de amplitud de fasor
        self.phasors_v = np.random.uniform(low=amplitude_min, high=amplitude_max, size=self.fps)        
        # array de frecuencia del fasor
        self.phasors_f = np.random.uniform(low=freq_min, high=freq_max, size=self.fps)

     
class ThreePhaseSineWave():
    """
    Representa una señal senoidal de tres canales.
    """
    def __init__(self, frequency: float, amplitude: tuple, phase: tuple, freq_noise:tuple, 
                 amp_noise:tuple, phase_noise:tuple, frames_p_sec:int ) -> None:
        self.frequency = frequency
        self.amplitude = amplitude
        self.phase = phase
        self.amp_noise=amp_noise
        self.freq_noise=freq_noise
        self.phase_noise = phase_noise
        self.fps=frames_p_sec
        self.phase1 = SineWave(frequency=self.frequency, amplitude=self.amplitude[0], 
                               phase=self.phase[0], freq_noise=self.freq_noise[0], 
                               amp_noise=self.amp_noise[0], phase_noise=self.phase_noise[0], 
                               frames_p_sec=self.fps)
        self.phase2 = SineWave(frequency=self.frequency, amplitude=self.amplitude[1], 
                               phase=self.phase[1], freq_noise=self.freq_noise[1], 
                               amp_noise=self.amp_noise[1], phase_noise=self.phase_noise[1], 
                               frames_p_sec=self.fps)
        self.phase3 = SineWave(frequency=self.frequency, amplitude=self.amplitude[2], 
                               phase=self.phase[2], freq_noise=self.freq_noise[2], 
                               amp_noise=self.amp_noise[2], phase_noise=self.phase_noise[2], 
                               frames_p_sec=self.fps)
        self.dataset_pmu = None
        self.generate_dataset()

    def generate_dataset(self):
        """Genera un dataframe segun la norma IEEE c37.118.2"""
        
        # Se generan los headers del dataframe
        headers = ['TimeStamp', 'Phase1', 'V1', 'Phase2', 'V2', 'Phase3', 
                   'V3', 'Freq', 'dFreq/dt']
        self.dataset_pmu = pd.DataFrame(columns=headers)
        
        # Estampa de tiempo
        # Genera el vector de tiempo en base a los frames/sec
        # Largo de vector: 1 s // paso:1/fps
        temp_vec=np.arange(0, 1 , 1/self.fps)
        # Obtiene la fecha y hora instantaneas      
        dt_now = datetime.now(tz=timezone.utc).timestamp()
        # Divide dt_now para obtener el inicio del segundo 
        dt_now_decimal, dt_now_entero = math.modf(dt_now)
        # Suma a la fecha y hora actual las fracciones de segundo surgidas de fps
        self.dataset_pmu['TimeStamp'] = [(dt_now_entero + dt) for dt in temp_vec]
        self.dataset_pmu['Phase1'] = self.phase1.phasors_phase
        self.dataset_pmu['V1'] = self.phase1.phasors_v 
        self.dataset_pmu['Phase2'] = self.phase2.phasors_phase
        self.dataset_pmu['V2'] = self.phase2.phasors_v
        self.dataset_pmu['Phase3'] = self.phase3.phasors_phase
        self.dataset_pmu['V3'] = self.phase3.phasors_v
        self.dataset_pmu['Freq'] = np.mean(np.array([self.phase1.phasors_f, 
                                                     self.phase2.phasors_f, 
                                                     self.phase3.phasors_f]), axis=0)
        
        self.dataset_pmu['dFreq/dt'] = np.zeros(self.fps)
      

# %% Prueba

# a=SineWave(frequency=50, amplitude=120, phase=0, freq_noise=5, amp_noise=0.25, 
#             phase_noise=2, frames_p_sec=10)
# b=ThreePhaseSineWave(frequency=50, amplitude=(120,120,120), phase=(0.01,120,240), 
#                       freq_noise=(0.2,0.2,0.2), amp_noise=(3,3,3), 
#                       phase_noise=(5,5,5), frames_p_sec=10)
# b.generate_dataset()
# c=b.dataset_pmu

