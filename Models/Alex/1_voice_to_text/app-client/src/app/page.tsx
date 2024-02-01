'use client'
import React, { useCallback, useEffect, useState } from 'react';
import Image from 'next/image'
import dynamic from 'next/dynamic';

import styles from './page.module.css'

// @ts-ignore
import { AudioVisualizer, LiveAudioVisualizer } from 'react-audio-visualize';
import { useAudioRecorder } from 'react-audio-voice-recorder';

const DynamicAudioRecorder = dynamic(
  () => import('react-audio-voice-recorder').then(mod => mod.AudioRecorder),
  { ssr: false }
);

const AudioRecord = ({ dimensions, sendAudioBlob }) => {
  const [blob, setBlob] = React.useState<Blob>();
  const recorder = useAudioRecorder();

  const divider = 0.6;

  const [width, setWidth] = useState(dimensions.width);
  const [height, setHeight] = useState(dimensions.height);

  useEffect(() => {
    setWidth(dimensions.width * divider);
    setHeight(dimensions.height * divider);
  }, [dimensions]);

  const addAudioElement = useCallback((blob) => {
    setBlob(blob);
    const url = URL.createObjectURL(blob);
    const audio = document.createElement("audio");
    audio.src = url;
    audio.controls = true;
    document.body.appendChild(audio);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", maxHeight: height }}>
      {blob && !recorder.mediaRecorder && (
        <AudioVisualizer
          blob={blob}
          width={500}
          height={500}
          barWidth={1}
          gap={0}
          barColor={'#f76565'}
        />
      )}
      {recorder.mediaRecorder && (
        <LiveAudioVisualizer
          mediaRecorder={recorder.mediaRecorder}
          width={width}
          height={height}
        />
      )}
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <DynamicAudioRecorder
          onRecordingComplete={addAudioElement}
          recorderControls={recorder}
          audioTrackConstraints={{
            noiseSuppression: true,
            echoCancellation: true,
          }}
          downloadOnSavePress={false}
          downloadFileExtension="webm"
        />
        {blob && !recorder.isRecording && !recorder.isPaused &&
          <input
            id={styles.SendButton}
            type="button"
            value="Envoyer"
            onClick={() => sendAudioBlob(blob)}
          />
        }
      </div>
    </div>
  );
};


export default function Home() {

  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    // Mettre à jour les dimensions lorsque la fenêtre est redimensionnée
    function handleResize() {
      setDimensions({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);

    // Nettoyer l'écouteur d'événement
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const sendAudioBlob = useCallback((audioBlob) => {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'audio.webm');

    fetch('http://localhost:4000/api/audio', {
      method: 'POST',
      body: formData,
    })

  }, []);

  return (
    <main className={styles.main}>
      <div className={styles.description}>
        <p>
          Get started to record your voice on clicking the microphone button below.
        </p>
        <div>
          <a
            href="http://localhost:3000/"
            target="_blank"
            rel="noopener noreferrer"
          >
            By{' Maverick Talys'}
            <Image
              src="/logo.svg"
              alt="Vercel Logo"
              className={styles.vercelLogo}
              width={100}
              height={50}
              priority
            />
          </a>
        </div>
      </div>
      <div>

      </div>
      <div>
        <AudioRecord dimensions={dimensions} sendAudioBlob={sendAudioBlob} />
      </div>
    </main>
  )
}
