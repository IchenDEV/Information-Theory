from decimal import Decimal
import decimal
decimal.getcontext().prec=1000
res=""
k=0
frequency_table ={} # 初始化频率表
for i in range(ord('a'),ord('z')+1):
    frequency_table[chr(i)]=1
frequency_table['#']=1
class ArithmeticEncoding:

    def get_probability_table(self, frequency_table):
        total_frequency = sum(list(frequency_table.values()))
        probability_table = {}
        for key, value in frequency_table.items():
            probability_table[key] = Decimal(value)/Decimal(total_frequency)
        return probability_table

    def get_encoded_value(self, last_stage_probs):
        last_stage_probs = list(last_stage_probs.values())
        last_stage_values = []
        for sublist in last_stage_probs:
            for element in sublist:
                last_stage_values.append(element)

        last_stage_min = min(last_stage_values)
        last_stage_max = max(last_stage_values)

        return (last_stage_min + last_stage_max)/2

    def process_stage(self, stage_min, stage_max):
        self.probability_table = self.get_probability_table(frequency_table)
        orimax=Decimal(stage_max)
        orimin=Decimal(stage_min)
        stage_probs = {}
        stage_domain = stage_max - stage_min
        ok=True
        for term_idx in range(len(self.probability_table.items())):
            term = list(self.probability_table.keys())[term_idx]
            term_prob = self.probability_table[term]
            cum_prob = term_prob * stage_domain + stage_min
            stage_probs[term] = [int(stage_min),int(cum_prob)]
            if int(stage_min)==int(cum_prob) or int(cum_prob) > orimax or int(stage_min)<orimin:
                ok=False
            stage_min = cum_prob
        return [stage_probs,ok]

    def encode(self, msg):
        # Make sure 
        msg = list(msg)
        encoder = []
        encoded_msg=''
        stage_min = 0
        stage_max = 2**64
        stage_probs={}
        tmpmsg=""
        for msg_term_idx in range(len(msg)):
            msg_term = msg[msg_term_idx]
            stage_probs,ok = self.process_stage(stage_min, stage_max)
            stage_min = stage_probs[msg_term][0]
            stage_max = stage_probs[msg_term][1]

            if(int(stage_min)>=int(stage_max)) or not ok:
                encoded_msg += tmpmsg
                #print(tmpmsg)
                stage_min=0
                stage_max=2**64
                stage_probs,ok = self.process_stage(stage_min, stage_max)
                stage_min = stage_probs[msg_term][0]
                stage_max = stage_probs[msg_term][1]

            #print(msg_term,"->",int(stage_min),int(stage_max))
            frequency_table[msg_term] += 1
            tmpmsg='0'*(64-len(bin(int(stage_min))[2:])) + bin(int(stage_min))[2:]
           
            if(msg_term == '#'):
                break
            
        encoded_msg += '0'*(64-len(bin(int((stage_min+stage_max)//2))[2:])) + bin(int((stage_min+stage_max)//2))[2:]

        return encoded_msg, encoder

    def decode(self, encoded_msg, msg_length):
        decoder = []
        decoded_msg = []
        for idx in range(1,int((msg_length-1)/64)+2):
            cmsg=encoded_msg[(idx-1)*64:idx*64]
            stage_min = 0
            stage_max = 2**64
            while True:
                stage_probs,ok = self.process_stage(stage_min, stage_max)
                for msg_term, value in stage_probs.items():
                    if int(cmsg,2) >= value[0] and int(cmsg,2) < value[1]:
                        break

                stage_min = stage_probs[msg_term][0]
                stage_max = stage_probs[msg_term][1]

                if(int(stage_min)==int(stage_max)) or not ok:

                    break
                #print(msg_term,"->",int(stage_min),int(stage_max))
                if(msg_term == '#'):
                    stage_min = 0
                    stage_max = 2**64
                    break
                decoded_msg.append(msg_term)
                frequency_table[msg_term] += 1


        return decoded_msg, decoder


original_msg = input("输入编码信息：")
print("原始信息: {msg}".format(msg=original_msg))
AE = ArithmeticEncoding()
encoded_msg, encoder = AE.encode(msg=original_msg)
print('编码信息:',encoded_msg)

frequency_table ={} # 重置频率表
for i in range(ord('a'),ord('z')+1):
    frequency_table[chr(i)]=1
frequency_table['#']=1
AE = ArithmeticEncoding()
decoded_msg, decoder = AE.decode(encoded_msg=encoded_msg, msg_length=len(encoded_msg))
print("解码信息: {msg}".format(msg=''.join(decoded_msg)))
