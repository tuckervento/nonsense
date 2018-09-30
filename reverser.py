import audioop
import wave
import readline
import cmd

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
        peak_duration = self.sample_file.getframerate()*self.sample_file.getnchannels()//1000*250
        #using audioop.findmax(fragment, length)
        global COUNT
        COUNT = 0
        peaks = _find_maxes(input_data, peak_duration, 0, len(input_data), num_peaks)
        #peaks = peaks[0:num_peaks]
        peaks.sort()
        insert = 0
        for i in range(num_peaks):
            start = insert*2
            stop = (peaks[i]+peak_duration)*2
            insert = peaks[i]+peak_duration
            self.output_data += audioop.reverse(input_data[start:stop],
                                                self.sample_file.getsampwidth())
        self.output_data += audioop.reverse(input_data[insert*2:],
                                            self.sample_file.getsampwidth())
        print('finished with data lengths: in: {} out: {}'.format(len(self.output_data),
                                                                  len(input_data)))
        #find the maximums, then search in the remaining data
        #continue until len(peaks) == num_peaks
        #build up output_data using audioop.reverse(fragment, sample_file.getsampwidth())
        return False
    
    def do_quit(self, arg):
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


cmd_loop = ReverseLoop()
cmd_loop.cmdloop()
