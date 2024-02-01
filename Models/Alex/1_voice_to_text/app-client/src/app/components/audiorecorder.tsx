// audiorecorder.tsx
import React, { useCallback } from "react";
import { AudioRecorder } from 'react-audio-voice-recorder';

export const AudioRecord = () => {
    const addAudioElement = useCallback((blob) => {
        const url = URL.createObjectURL(blob);
        const audio = document.createElement("audio");
        audio.src = url;
        audio.controls = true;
        document.body.appendChild(audio);
    }, []);

    return (
        <AudioRecorder
            onRecordingComplete={addAudioElement}
            audioTrackConstraints={{
                noiseSuppression: true,
                echoCancellation: true,
            }}
            downloadOnSavePress={true}
            downloadFileExtension="webm"
        />
    );
};

// Marquer le composant comme client
const ClientAudioRecord = client(AudioRecord);

export default ClientAudioRecord;
