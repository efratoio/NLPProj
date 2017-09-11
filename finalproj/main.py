import data
import network
import sys
from os import listdir, path
from contextlib import redirect_stdout

class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

    def close(self):
    	self.log.close()

def evaluate_model(config,model,x_train, y_train,x_val, y_val,x_test,y_test):
    print(model.metrics_names)
    if config["PROPS"]:
    	model.fit([x_train[0],x_train[1]], y_train, validation_data=([x_val[0],x_val[1]], y_val),epochs=10, batch_size=20)
    else:
	    model.fit(x_train, y_train, validation_data=(x_val, y_val),epochs=config["EPOCHS"], batch_size=config["BATCH_SIZE"])

    return model.evaluate(x_test,y_test, batch_size=config["BATCH_SIZE"], verbose=1, sample_weight=None)



def run_net(config,word_index,x_train, y_train,x_val, y_val,x_test,y_test):
	model = network.create_network(config,word_index)
	res = evaluate_model(config,model,x_train, y_train,x_val, y_val,x_test,y_test)
	print(str(net)+"\n")
	print(str(res)+"\n")

  


  
def run_network(config):
	chats = data.gen_chat_data()
	word_index,x_train, y_train,x_val, y_val,x_test,y_test = data.prepare_datasets(config,chats)     
	run_net(config,word_index,x_train, y_train,x_val, y_val,x_test,y_test)




for file_name in listdir("./configurations"):
	with open(path.join("./experiments",file_name[:-5]+".log"),"w") as log_file:
		with redirect_stdout(log_file):
			config = data.load_config(path.join("./configurations",file_name))
			print("hi")
			try:
				run_network(config)
			except:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				print("Unexpected error: %s %s %s"%(exc_type, exc_value, exc_traceback))

