Skript basiert auf dem fft-hue Skript von alelouis
Es ist noch am Anfang der Entwicklung als Alpha bzw. nur zum Testen. Jeder kann hier gern seinen Senf dazugeben.

Skript-Änderungen:
Berechnung des Peak
Auf dem Bildschirm wird der Peak als Balken angezeigt
Es gibt eine automatische Lautstärkeanpassung bis auf eine bestimmte MIndestlautstärke, die ist natürlich von dem verwendeten Mikrofon abhängig. Das Device wird manuell in der Zeile

stream=p.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=chunk, input_device_index=2)

festgelegt. Die Rate ist hier manuell eingetragen, um damit etwas zu experimentieren.

Ich benutze das Skript mit einer Hue-Bridge v1. Deswegen kommen die Signale noch etwas träge an den Lichtern an und ab > 2 Leuchten passt der Takt nicht mehr. Besorge mir demnächst eine aktuell Bridge.

Folgende Varianten wünsche ich mir für dieses Tool:
Im Moment rotieren die Farbwerte einfach nur und die Helligkeit wird durch die Lautstärke beeinflusst. Ich möchte, dass die Lampen ihre Farbe nach der Frequenz wechseln oder verschiedene Lampen sich nach verschiedenen Frequenzen (bass, mid, treble) richten.


# fft-hue

Python script based on Fast Fourier Transform to dynamically animate your Philips Hue lights.
***
### How-to
1. Install dependencies `pip install requests pyaudio numpy`
2. Create an authenticated user for your Hue Bridge : [Philips' tutorial](https://www.developers.meethue.com/documentation/getting-started)
3. Add your devices/lights following this synthax (changing `/lights/1/state`)
  ```Python
  r_1 = requests.put('http://' + hue_bridge_ip + '/api/' + user_id 
  +'/lights/1/state', data='{"bri": ' + str(bri) +', "transitiontime" : 1, "hue": ' + hue +'}')
  ```
4. Run script `python fft-hue-debug.py`
5. Make some noises
***
### Tweakings
Sound sensibility can be adjusted with the `activation_threshold` variable.

Modify `input_device_index` to choose the audio device streamed. Open a Python shell with `pyaudio.PyAudio().get_device_info_by_index(N)` to check your available devices.
***
### Dependencies
* [requests](http://docs.python-requests.org/en/master/) : HTTP Library *(send requests to Hue Bridge)*
* [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) : Audio Library *(open audio streams)*
* [numpy](http://www.numpy.org/) : Scientific Library *(fft and data manipulation)*

