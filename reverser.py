import audioop
import wave
import readline
import cmd
import sys
import math

class ReverseLoop(cmd.Cmd):
    intro = 'Welcome to the MaxReverser.  Enter \'help\' for a list of commands'
    prompt = '($$$)-> '
    sample_file = None #filled with load_file command
    output_device = None #filled with load_device command
    output_data = None #filled with process command

    def do_load_file(self, arg):
        '''
        Load the file from the specified path.

        Args:
            path - absolute path to a .wav file
        '''
        self.sample_file = wave.open(arg, mode='rb')
        return False

    def do_write_file(self, arg):
        '''
        Write the current output data to the specified path.

        Args:
            path - absolute path to a new .wav file
        '''
        output_file = wave.open(arg, mode='wb')
        output_file.setparams(self.sample_file.getparams())
        output_file.writeframes(self.output_data)
        output_file.close()
        return False

    def do_process(self, arg):
        num_peaks = int(arg)
        self.sample_file.rewind()
        self.output_data = b''
        input_data = self.sample_file.readframes(self.sample_file.getnframes())
        peak_duration = int(self.sample_file.getframerate()*self.sample_file.getnchannels()/1000*250)
        #using audioop.findmax(fragment, length)
        global COUNT
        COUNT = 0
        #peaks = _find_maxes(input_data, peak_duration, 0, len(input_data), num_peaks)
        peaks = [audioop.findmax(input_data, peak_duration)] 
        width = self.sample_file.getsampwidth()
        for i in range(num_peaks):
            start = 0
            end = len(input_data)
            temp_peaks = []
            for j in range(len(peaks)):
                if peaks[j]*width-start > peak_duration*width:
                    temp_peaks.append(audioop.findmax(input_data[start:peaks[j]*width], peak_duration))
                start = (peaks[j]+peak_duration)*width
            if len(input_data)-start > peak_duration*width:
                temp_peaks.append(audioop.findmax(input_data[start:], peak_duration))
            peaks.extend(temp_peaks)
            peaks.sort()
            print('------------------------------------------------')
            print('found new peaks: {}\n{} remain'.format(temp_peaks, num_peaks-len(peaks)))
            if len(peaks) >= num_peaks:
                break
        peaks.sort()
        insert = 0
        print('------------------------------------------------')
        print('reversing!')
        output = []
        for i in range(len(peaks)):
            if i%50==0:
                print('reversing up to peak {}: {}'.format(i, peaks[i]))
            start = insert*width
            insert = peaks[i] + peak_duration
            stop = insert*width
            stop += start-stop%width
            output.append(audioop.reverse(input_data[start:stop], width))
        output.append(audioop.reverse(input_data[insert*2:], width))
        self.output_data = b''.join(output)
        print('finished with data lengths: in: {} out: {}'.format(len(self.output_data),
                                                                  len(input_data)))
        #find the maximums, then search in the remaining data
        #continue until len(peaks) == num_peaks
        #build up output_data using audioop.reverse(fragment, sample_file.getsampwidth())
        return False
    
    def do_quit(self, arg):
        if self.sample_file is not None:
            self.sample_file.close()
        return True

COUNT = 0

def _find_maxes(data, duration, start, stop, num):
    global COUNT
    return_list = []
    if stop - start < duration:
        return return_list
    try:
        m = audioop.findmax(data[start:stop], duration)
    except audioop.error:
        print('got an error with data: {} {}'.format(start, stop))
        return return_list
    COUNT+=1
    return_list.append(m)
    if COUNT < num:
        return_list.extend(_find_maxes(data, duration, start, m*2, num))
        return_list.extend(_find_maxes(data, duration, (m+duration)*2, stop, num))
    return return_list


def _load_output_device(name):
    return #handle?


if __name__ == '__main__':
    cmd_loop = ReverseLoop()
    if len(sys.argv) > 1:
        cmds = sys.argv[1:]
        for i in range(math.ceil(len(cmds)/2)):
            this_cmd = ' '.join(cmds[i*2:i*2+2])
            print('executing {}'.format(this_cmd))
            cmd_loop.onecmd(this_cmd)
    else:
        cmd_loop.cmdloop()
