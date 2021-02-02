import libs.game as game
import pygame
import random


mp= {0:(1,3,5,6,8,10,12,13),
     1:(14,15)}

class Generate_music:
    def __init__(self):
        self.prev_pitches=[]
        self.pitch=None
        self.modes= (
                (1,3,5,6,8,10,12,13,15,17,18,20,22,24,25),
                (1,3,4,6,8,9,11,13,15,16,18,20,21,23,25)
                    )
        self.chords=(
                    (1,3,5,8),
                    (3,5,8,10),
                    (5,8,10,12),
                    (1,3,5,7),
                    (3,5,7,8),
                    (5,7,8,10),
                    (7,8,10,12),
                    (1,5,9,13)
                    )

        self.key=[]
        self.count_single=0
        self.count_key=0
        self.count_chord=0
        self.mode=[]
        self.skale=[]
        self.chord=None
        self.chord_pitch=None
        self.change_key()

    def change_key(self):
        self.count_single+=1
        self.mode=list(self.modes[random.randint(0,len(self.modes)-1)])
        self.skale.clear()
        transp=random.randint(0,11)

        for i in range(0,len(self.mode)-1):
            if self.mode[i] + transp > 25:
                self.mode[i]=self.mode[i]-24+transp
            else:
                self.mode[i]+=transp
            self.skale.append(self.mode[i])

        self.count_key=0
        print('Skale: ',self.skale)

    def play_single(self,idx=-1):
        self.count_key+=1
        while True:
            self.pitch=self.skale[random.randint(0,len(self.skale)-1)]
            if not self.pitch in self.prev_pitches and abs(self.pitch-idx)>2:
                break
        game.musicsnd[self.pitch-1].stop()
        game.musicsnd[self.pitch-1].play()
        game.musicsnd[self.pitch-1].set_volume(0.5)

        self.prev_pitches.append(self.pitch)
        if len(self.prev_pitches) >3:
            self.prev_pitches.remove(self.prev_pitches[0])

        #if self.count_single == 1:
        #    self.play_single(self.pitch)
        #elif self.count_single == 2:
        #    self.count_single=0


    def change_chord(self,transp=-1,form='random'):
        print('Chord type: ',form)
        if transp==-1:
            transp=random.randint(0,len(self.skale)-1)

        if form=='random':
            self.chord = list(self.chords[random.randint(0,len(self.chords)-2)])
        elif form == 'triad':
            self.chord = list(self.chords[random.randint(0, len(self.chords) - 6)])
        elif form == 'sept':
            self.chord = list(self.chords[random.randint(3, len(self.chords) - 2)])
        elif form == 'disson':
            self.chord = list(self.chords[len(self.chords)-1])
        else:
            self.chord=list(self.chords[0])
        print('Chord: ',self.chord)

        for i in range(0, len(self.chord)-1):
            if self.chord[i]+transp > len(self.skale):
                self.chord[i] = self.chord[i] - len(self.skale) +transp
            else:
                self.chord[i] = self.chord[i]+transp



    def play_chord_block(self):
        self.count_chord += 1

        self.pitch=self.skale[self.chord[self.count_chord-1]-1]
        game.musicsnd[self.pitch-1].stop()
        game.musicsnd[self.pitch-1].play()
        game.musicsnd[self.pitch-1].set_volume(0.3)

        self.prev_pitches.append(self.pitch)
        if len(self.prev_pitches) >3:
            self.prev_pitches.remove(self.prev_pitches[0])

        if self.count_chord < len(self.chord):
            self.play_chord_block()
        elif self.count_chord == len(self.chord):
            self.count_chord=0
