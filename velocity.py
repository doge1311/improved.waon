import argparse
import mido

def extract_notes_from_midi(midi_file):
    notes = []
    max_velocity = 0
    mid = mido.MidiFile(midi_file)
    for track in mid.tracks:
        current_time = 0
        for msg in track:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity != 0:  # Note-on
                notes.append((msg.note, current_time, msg.velocity, 'on'))
                if msg.velocity > max_velocity:
                    max_velocity = msg.velocity
            elif (msg.type == 'note_on' and msg.velocity == 0) or msg.type == 'note_off':  # Note-off
                notes.append((msg.note, current_time, msg.velocity, 'off'))
    return notes, max_velocity

def distribute_notes_to_tracks(notes, max_velocity, num_tracks):
    tracks = [[] for _ in range(num_tracks)]  # Initialize tracks
    active_notes = {}
    
    for note in notes:
        note_pitch = note[0]
        event_time = note[1]
        velocity = note[2]
        event_type = note[3]
        
        # Scale velocity to the range [0, 127]
        scaled_velocity = int((velocity / max_velocity) * 127)

        if event_type == 'on':
            track_index = min(scaled_velocity // (128 // num_tracks), num_tracks - 1)  # Distribute based on scaled velocity range
            tracks[track_index].append((note_pitch, event_time, scaled_velocity, 'on'))
            active_notes[note_pitch] = track_index
        elif event_type == 'off' and note_pitch in active_notes:
            track_index = active_notes[note_pitch]
            tracks[track_index].append((note_pitch, event_time, scaled_velocity, 'off'))
            del active_notes[note_pitch]

    return tracks

def write_midi_file(tracks, output_file, ticks_per_beat):
    mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    for track_index, track_notes in enumerate(tracks):
        if track_notes:  # Check if track has any notes
            track = mido.MidiTrack()
            mid.tracks.append(track)
            prev_time = 0
            for note in track_notes:
                delta_time = note[1] - prev_time
                if note[3] == 'on':
                    note_on = mido.Message('note_on', note=note[0], velocity=note[2], time=delta_time)
                    track.append(note_on)
                else:
                    note_off = mido.Message('note_off', note=note[0], velocity=note[2], time=delta_time)
                    track.append(note_off)
                prev_time = note[1]
    
    mid.save(output_file)

def main(input_midi_file, output_midi_file, num_tracks):
    # Read the input MIDI file to get ticks per beat
    mid = mido.MidiFile(input_midi_file)
    ticks_per_beat = mid.ticks_per_beat

    notes, max_velocity = extract_notes_from_midi(input_midi_file)
    tracks = distribute_notes_to_tracks(notes, max_velocity, num_tracks)
    write_midi_file(tracks, output_midi_file, ticks_per_beat)

    print("Output MIDI file generated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distribute MIDI notes to tracks.")
    parser.add_argument("input_file", help="Path to the input .mid file")
    parser.add_argument("output_file", help="Path for the output .mid file")
    parser.add_argument("num_tracks", type=int, help="Number of tracks")

    args = parser.parse_args()

    main(args.input_file, args.output_file, args.num_tracks)
