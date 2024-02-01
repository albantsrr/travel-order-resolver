import fs from "fs";
import path from "path";
import dotenv from 'dotenv';

import Express from "express";
import cors from "cors";
import multer from "multer";

import Ffmpeg from "fluent-ffmpeg";

import speech from '@google-cloud/speech';


dotenv.config();

const app = Express();
const port = 4000;

const upload = multer()

const credentialsBase64 = process.env.GOOGLE_CREDENTIALS;
console.log('[SERVER LOG] - GOOGLE_CREDENTIALS - ', credentialsBase64);
if (!credentialsBase64) {
    throw new Error('GOOGLE_CREDENTIALS env variable is missing');
}
const credentialsJSON = Buffer.from(credentialsBase64, 'base64').toString('utf8');
const credentials = JSON.parse(credentialsJSON);
const googleClient = new speech.SpeechClient({ credentials });


app.use(cors({
    origin: 'http://localhost:3000'
}));

// ? Send audio recorder from client
app.post('/api/audio', upload.single('audio'), async (req, res) => {

    console.log('API AUDIO RECEIVED', req.file);

    const audioBuffer = req.file.buffer;
    console.log('[SERVER LOG] Retrieve audio buffer');
    const inputPath = path.join('./temp', 'input.webm');
    console.log('[SERVER LOG] Input file path: ', inputPath);
    const outputPath = path.join('./audios', 'audio.flac');
    console.log('[SERVER LOG] Output file path: ', outputPath);

    fs.writeFileSync(inputPath, audioBuffer);
    console.log('[SERVER LOG] IS TEMP AUDIO FILE CREATED ? ', fs.existsSync(inputPath));

    Ffmpeg()
        .input(inputPath)
        .toFormat('flac')
        .on('end', () => {
            fs.unlinkSync(inputPath);
            console.log('[SERVER LOG] IS TEMP AUDIO FILE DELETED ? ', !fs.existsSync(inputPath));
        })
        .on('error', (err) => {
            throw new Error('[SERVER LOG] - ERROR - Error during conversion: ' + err.message);
        })
        .save(outputPath);

    // Send audio to Google Cloud Speech API for transcription
    const file = fs.readFileSync(outputPath);
    const audioBytes = file.toString('base64');
    const audio = {
        content: audioBytes,
    }
    const config = {
        encoding: 'FLAC',
        sampleRateHertz: 48000,
        languageCode: 'fr-FR',
    }
    const request = {
        audio,
        config,
    }

    const [response] = await googleClient.recognize(request);
    console.log('[SERVER LOG] - RESPONSE - ', response);
    if (response.results.length > 0) {
        const transcription = response.results.map(result => result.alternatives[0].transcript).join('\n');
        console.log('[SERVER LOG] - TRANSCRIPTION - ', transcription);
    }
    res.send('Post request received!')
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});