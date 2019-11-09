import os

import tkinter 					# Для создания оконного интерфейса

import soundfile as sf			# Для обработки аудио

import moviepy.editor as mp		# Для выделения аудодорожки из аудио

from pydub import AudioSegment 	# Для преобразования аудио

import matplotlib.pyplot as plt # Для построения графиков

from scipy.fftpack import fft	# Для БПФ преобразования

from pylab import*				#

from scipy.io import wavfile	# Для преобразования аудио

import numpy					# Для Обработки аудио
####Элементы интерфейса
###Окна
script_path = os.path.dirname(os.path.abspath(__file__))
#Главное окно
root = tkinter.Tk()
root.title("Главное меню")
root.geometry('1024x768')
root.resizable(False,False)
#Задний фон
bg_image = tkinter.PhotoImage( file = script_path + '\\bg.png' )
bg_canvas = tkinter.Canvas( root )
bg_label = tkinter.Label( root, text = '', image = bg_image)

#Элементы главного окна
##Надписи
titleText = tkinter.Label(root, text = "Проверка аудиофайла", font='arial 42')
inputText = tkinter.Label( root, text = "Загрузка аудиофайла", font = "arial 42" )
entryLegend = tkinter.Label( root, text = "Введите путь к файлу:", font = 'arial 16'  )
input_k_legend = tkinter.Label( root, text = "Введите точность сравнения:", font = 'arial 16' )
error_label = tkinter.Label( root, text = "Ошибка! Проверьте правильность введённых данных" )
loading_Label = tkinter.Label( root, text = "Подождите. Файл обрабатывается" )
lower_amp_label = tkinter.Label( root, text = "Введите нижний диапазон:", font = 'arial 16' )

##Кнопки
mainButton = tkinter.Button( root, width= 35 , bg = 'gray', text = 'Загрузить файл', height = 3 , font="arial 32")
goBackButton = tkinter.Button( root, width = 10, height = 2, text = "Назад", font = "arial 16", bg = "gray" )
runButton = tkinter.Button( root, width = 5, height = 2, bg = "gray", text = "OK", font = "arial 12" )

##Поля ввода
inputField = tkinter.Entry( root, width = 65 )
input_k_field = tkinter.Entry( root, width = 15 )
lower_amp_entry = tkinter.Entry( root, width = 15 )

#Размещение элементов
titleText.pack()
mainButton.pack()

#Переменные 
data = []
result = []
samplerate = 0

##Действия при нажатии кнопок
def PressMainButton( event ):
	"""
	Действие при нажатии главной кнопки
	"""
	print("Pressed Main button")
	titleText.pack_forget()
	mainButton.pack_forget()
	inputText.pack()
	entryLegend.place( x = 50, y = 225 )
	goBackButton.place( x = 50, y = 400 )
	inputField.place( x = 360, y = 230 )
	input_k_legend.place( x = 50, y = 295 )
	input_k_field.place( x = 360, y = 300  )
	lower_amp_label.place( x = 50, y = 260 )
	lower_amp_entry.place( x = 360, y = 265 )
	runButton.place( x = 500 , y = 270 )
	pass
mainButton.bind( '<Button-1>', PressMainButton )

def PressBackButton( event ):
	"""
	Действие при нажатии кнопки назад
	"""
	print( "Pressed back button" )
	inputText.pack_forget()
	entryLegend.place_forget()
	goBackButton.place_forget()
	inputField.place_forget( )
	runButton.place_forget( )
	input_k_legend.place_forget()
	input_k_field.place_forget()
	lower_amp_label.place_forget()
	lower_amp_entry.place_forget()
	titleText.pack( )
	mainButton.pack( )
goBackButton.bind( '<Button-1>', PressBackButton )

#Функция обрабоотчик аудиопотока
def PressRunButton( event ):
	"""
	Действие при потверждении ввода
	"""
	print( "Running script" )
	global result, fft_result_show, data, samplerate

	#Очистка  данных
	result.clear()
	data = numpy.array( [] )
	samplerate = 0
	#C:\Users\User\Desktop\icons\CourceWork\test\ConvertionTest\test3.mp3
	#C:\Users\User\Desktop\icons\CourceWork\src\binaural.wav
	#C:\Users\User\Desktop\icons\CourceWork\test\ConvertionTest\test_v1.mp4
	#C:\Users\User\Desktop\icons\CourceWork\test\ConvertionTest\bells.mp3
	#C:\Users\User\Desktop\icons\CourceWork\test\ConvertionTest\water01.mp3
	#C:\Users\User\Desktop\icons\CourceWork\test\ConvertionTest\test_binaural_1.mp3

	#Преобразование файла в wav
	try:
		_path_ = inputField.get()
		print(_path_)
		TMP_FILE = script_path + '\\src\\test.wav'
		if '.mp4' in _path_:
			mp4_to_wav(_path_, TMP_FILE)
		else:
			mp3_to_wav( _path_, TMP_FILE )
		#Обработка данных аудио
		data, samplerate = sf.read( TMP_FILE )
		print( samplerate )
	except:
		error_label.place( x = 50, y = 350  )
		return -1
	k = 1
	if input_k_field.get() != '':
		k = float( input_k_field.get() )
	lower = 20.0
	if lower_amp_entry.get() != '':
		lower = float( lower_amp_entry.get() )
	seconds = len( data ) // samplerate
	print( 'Обработка аудиофайла' )
	print( 'Частота дискретизации: ' )
	print( 'Нижний диапазон: ' + str( lower ) )
	print( 'Количество секунд: ' + str( seconds ) )
	print( 'Точность сравнения: ' + str( k ) )
	for second in range( seconds ):
		_1_second_res = binaural_search_in_1_second( data, samplerate, second, k, lower )
		result.append( _1_second_res )
		print( 'Обработано секунд: ' + str( second ) )
	goBackButton.place()
	runButton.place( )

	#Окно результата программы
	runWindow = tkinter.Tk()
	runWindow.title( "Резултат выполнения программы" )
	runWindow.geometry('1024x768')
	runWindow.resizable(False,False)
	#Элементы интерфейса result_ruut

	###Показать график одной секунды
	res_label = tkinter.Label( runWindow, text = 'Результат анализа аудиофайла', font = 'Arial 46' )
	show_second_label = tkinter.Label( runWindow, text = 'Посмотреть график одной секунды', font = 'Arial 20'  )
	show_second_button = tkinter.Button( runWindow, width = 4, height  = 2 , text = 'OK' )
	enter_second_label = tkinter.Label( runWindow, text = "Введите номер секунды:", font = 'arial 12' )
	enter_second_field = tkinter.Entry( runWindow, width = 10 )

	##Показать БПФ одной секунды:
	show_second_label_fft = tkinter.Label( runWindow, text = 'Посмотреть БПФ график одной секунды',  font = 'Arial 20' )
	show_second_button_fft = tkinter.Button( runWindow, width = 4, height  = 2 , text = 'OK' )
	enter_second_label_fft = tkinter.Label( runWindow, text = "Введите номер секунды:", font = 'arial 12' )
	enter_second_field_fft = tkinter.Entry( runWindow, width = 10 )

	##Показать результат исследования:
	show_res_label = tkinter.Label( runWindow, text = 'Показать результат анализа', font = 'Arial 20' )
	show_res_button = tkinter.Button( runWindow, width = 4, height  = 2 , text = 'OK' )
	enter_delta_label_res = tkinter.Label( runWindow, text = "Введите нужную разность частот:", font = 'arial 12' )
	enter_delta_field_res = tkinter.Entry( runWindow, width = 10 )

	#Размещение элементов на экране
	##
	res_label.pack(  )
	show_second_label.place( x = 50, y = 100 )
	enter_second_label.place( x = 50, y = 140 )
	enter_second_field.place( x = 300, y = 140 )
	show_second_button.place( x = 570, y = 110 )
	##
	show_second_label_fft.place( x = 50, y = 175 )
	enter_second_label_fft.place( x = 50, y = 205 )
	enter_second_field_fft.place( x = 300, y = 205 )
	show_second_button_fft.place( x = 570, y = 185 )
	##
	show_res_label.place( x = 50, y = 250 )
	enter_delta_label_res.place( x = 50, y = 280 )
	enter_delta_field_res.place( x = 300, y = 280 )
	show_res_button.place( x = 570, y = 265 )

	#Действия при нажатии кнопок
	def show_1sec_audio( event ):
		"""
		Строит и отображает график одной секунды аудио
		"""
		global data, samplerate
		left = [ x[0]  for x in data ]
		right = [ x[1]  for x in data ]
		if enter_second_field.get() != '':
			second = int( enter_second_field.get() )
			plt.plot( left[ samplerate * second: samplerate * ( second + 1 ) ], 'r' )
			plt.plot( right[ samplerate * second: samplerate * ( second + 1 ) ], 'b' )
			plt.show()
		else:
			plt.plot( left[ 0: samplerate ] , 'r' )
			plt.plot( right[ 0: samplerate ] , 'b' )
			plt.show()
		pass
	show_second_button.bind( '<Button-1>', show_1sec_audio )

	#
	def show_fft_1sec_audio( event ):
		"""
		Строит и отображает БПФ график одной секунды аудио
		"""
		global data, samplerate
		second = 0
		if enter_second_field_fft.get() != '':
			second = int( enter_second_field_fft.get() )
		left = [ x[ 0 ] for x in data[ samplerate * second : samplerate * ( second + 1 ) ] ] 
		right = [ x[ 1 ] for x in data[ samplerate * second : samplerate * ( second + 1 ) ] ] 
		fft_left = fft( left, samplerate )
		fft_right = fft( right, samplerate )
		plt.plot( [ abs( x.real ) for x in fft_left[ 0 : samplerate // 2 ] ], 'ro' )
		plt.plot( [ abs( x.real ) for x in fft_right[ 0 : samplerate // 2 ] ], 'bo' )
		plt.show()
	show_second_button_fft.bind( '<Button-1>', show_fft_1sec_audio )

	#
	def show_result( event, second = -1 ):
		"""
		Показывает результат обработки аудиодорожки
		"""
		global result
		print( result )
		print( len( result ) )
		delta = 10
		leng = len( result )
		out = [ 0 * x  for x in range( leng ) ]
		i = 0
		if enter_delta_field_res.get() != '':
			delta = int( enter_delta_field_res.get() )
		print( delta )
		for second_res in result:
			for elem in second_res:
				if elem == delta:
					out[ i ] = elem
			i+=1
		print( len( out ) )
		plt.plot( out, 'go' )
		plt.show()
		out.clear()
		pass
	show_res_button.bind( '<Button-1>', show_result )

runButton.bind( '<Button-1>', PressRunButton )

#Функции обработки аудио
def mp4_to_wav(_src_ , _wav_):
	"""
	Выделяет звук из видеофайла
	"""
	videoclip = mp.VideoFileClip(_src_)
	audioclip = videoclip.audio.write_audiofile(_wav_)

def mp3_to_wav( _src_ ,  _dst_  ):
	"""
	Преобразует mp3 в wav
	"""                                        
	sound = AudioSegment.from_mp3( _src_ )
	sound.export( _dst_, format="wav") 

def binaural_search_in_1_second ( data, samplerate, second , k , lower  ):
	"""
	Ищет бинауральные ритмы в 1 с аудио
	"""
	res = []
	data1 = data[ samplerate * second : samplerate * ( second + 1 ) ]

	#Преобразование Фурье
	left = [ x[0]  for x in data1 ]
	right = [ x[1]  for x in data1 ]
	fft_left = fft( left, samplerate )
	fft_right = fft( right, samplerate )
	fft_left_normalize = [ abs( x.real ) for x in fft_left[ :2000  ] ]
	fft_right_normalize = [ abs( x.real ) for x in fft_right[ : 2000  ] ]

	#Поиск бинауральных ритмов
	for i in range( 1975 ):
		if abs( fft_right_normalize[ i ] ) >= lower:
			for j in range ( i + 1 , i + 26 ):
				if abs( fft_left_normalize[ j ] ) >= lower:
					if ( abs( fft_right_normalize[ i ] - fft_left_normalize[ j ] ) <=  k ):
						res.append(j - i) 

	print( 'XXXXXXXXXXXXXXXXXXXXXXXXXXX' )
	for i in range( 1975 ):
		if abs( fft_left_normalize[ i ] ) >= lower:
			for j in range ( i + 1 , i + 26 ):
				if abs( fft_right_normalize[ j ] ) >= lower:
					if ( abs( fft_right_normalize[ j ] - fft_left_normalize[ i ] ) <=  k ):
						res.append(j - i) 
	return res	

bg_label.place( x = 0, y = 0, relheight = 1, relwidth = 1 )
bg_canvas.place( x = 0, y = 0 )
root.mainloop()











