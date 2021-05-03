from flask import Flask, render_template, request
from pytube import YouTube
from flask import send_file
from unicodedata import normalize
import os
import re


app = Flask(__name__)

def formata_nome_arquivo (nome_arquivo)-> str:
    nome_arquivo = normalize('NFKD', nome_arquivo).encode('ASCII', 'ignore').decode('ASCII')
    return nome_arquivo


@app.route('/')
def av_download():
    nome_arquivo = ''
    url_tube = request.args.get('url')
    if url_tube:
        download(url_tube)
        yt = YouTube(url_tube)
        nome_arquivo = yt.title
    return render_template('index.html',  audio_donwload=nome_arquivo, video_donwload=nome_arquivo)


def download(url_tube):
    yt = YouTube(url_tube)
    nome_arquivo = yt.title
    nome_arquivo_formatado = formata_nome_arquivo(nome_arquivo)

    filtro_video = yt.streams.filter(progressive=True, file_extension='mp4')
    filtro_video.first().download(output_path='file_temp_video/', filename=nome_arquivo_formatado)

    filtro_audio = yt.streams.filter(only_audio=True, mime_type='audio/mp4')
    filtro_audio.first().download(output_path='file_temp_audio/', filename=nome_arquivo_formatado)
    path_mp4 = 'file_temp_audio/' + nome_arquivo_formatado + '.mp4'
    path_mp3 = 'file_temp_audio/' + nome_arquivo_formatado + '.mp3'
    os.rename(path_mp4, path_mp3)


@app.route('/download')
def link_download_file():
    midia = request.args.get('midia')
    nome_midia = request.args.get('nome_midia')
    nome_midia = formata_nome_arquivo(nome_midia)
    if midia =='audio':
        return send_file('file_temp_audio\\' + nome_midia + '.mp3', as_attachment=True)
    else:
        return send_file('file_temp_video\\' + nome_midia + '.mp4', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
