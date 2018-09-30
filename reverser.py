import audioop
import wave
import readline
import cmd

class ReverseLoop(cmd.Cmd):
    intro = 'Welcome to the MaxReverser.  Enter `'help`' for a list of commands'
    prompt = '($$$)'
    sample_file = None #filled with load_file command
    output_device = None #filled with load_device command
    output_data = None #filled with process command

    def do_load_file(self, arg):
        '''
        Load the file from the specified path.

        Args:
            path - absolute path to a .wav file
        '''
        sample_file = wave.open(arg, mode='rb')
        return False

    def do_write_file(self, arg):
        '''
        Write the current output data to the specified path.

        Args:
            path - absolute path to a new .wav file
        '''
        output_file = wave.open(arg, mode='wb')
        output_file.setparams(sample_file.getparams())
        output_file.writeframes(output_data)
        output_file.close()
        return False

#    def do_load_device(self, arg):
#        return False

    def do_process(self, arg):
        num_peaks = int(arg)
        sample_file.rewind()
        input_data = sample_file.readframes(sample_file.getnframes())
        peak_duration = sample_file.getframerate() * sample_file.getnchannels() // 1000 * 250
        #using audioop.findmax(fragment, length)
        peaks = _find_max(input_data, peak_duration, 
        first_index = audioop.findmax(input_data, peak_duration)
        second_index = audioop.findmax(input_data[0:first_index], peak_duration)
        third_index = audioop.findmax(input_data[first_index+peak_duration], peak_duration)
        #find the maximums, then search in the remaining data
        #continue until len(peaks) == num_peaks
        #build up output_data using audioop.reverse(fragment, sample_file.getsampwidth())
        return False

    def _find_max(data, duration, start, stop):
        return_list = []
        if stop - start < duration:
            return return_list
        return_list.append(audioop.findmax(data[start:stop], duration))
        return_list.extend(_find_max(data, duration, start, i*2))
        return_list.extend(_find_max(data, duration, (i+duration)*2, stop))
        return return_list

#    def do_play(self, arg):
#        return False

#    def do_stop(self, arg):
#        return False

    def do_quit(self, arg):
        self.do_stop(arg)
        return True


def _load_file(path):

def _load_output_device(name):
    return #handle?


cmd_loop = ReverseLoop()
cmd_loop.cmdloop()


