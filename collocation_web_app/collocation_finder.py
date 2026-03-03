import re
import math
from collections import Counter
from typing import List, Dict, Tuple

class CollocationFinder:
        
    def __init__(self):
        self.stopwords = self._get_stopwords()
        self.prepositions = {'в', 'на', 'с', 'у', 'к', 'о', 'об', 'по', 'за', 'над', 'под', 'без', 'для', 'до', 'из', 'от', 'про'}
        self.conjunctions = {'и', 'а', 'но', 'да', 'или', 'то', 'чтобы', 'что'}
        self.pronouns = {'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они', 'мой', 'твой', 'свой', 'наш', 'ваш', 'его', 'ее', 'их'}
        self.adverbs = {'очень', 'слишком', 'так', 'такой', 'такая', 'такое', 'такие', 'более', 'менее', 'здесь', 'там', 'тут', 'всегда', 'никогда', 'быстро', 'медленно', 'громко', 'тихо', 'весело', 'грустно'}
        
        self.boring_words = {
            'это', 'был', 'была', 'было', 'были', 'быть',
            'его', 'ее', 'их', 'все', 'она', 'они', 'оно',
            'вот', 'так', 'как', 'что', 'чтобы', 'потому',
            'когда', 'уже', 'еще', 'там', 'тут', 'здесь',
            'очень', 'совсем', 'вдруг', 'опять', 'тоже',
            'ведь', 'даже', 'только', 'почти', 'наконец',
            'можно', 'надо', 'нужно', 'нельзя', 'конечно',
            'того', 'этого', 'этому', 'этим', 'этом',
            'себя', 'тебя', 'меня', 'вас', 'нам', 'вам',
            'них', 'него', 'нему', 'ней', 'нею', 'ними'
        }
        
        self.bad_patterns = [
            ('назад', 'тому'),
            ('том', 'моя'),
            ('терпеть', 'или'),
            ('него', 'глядела'),
            ('плечах', 'несмотря'),
            ('наверчено', 'какое'),
            ('белобрысые', 'мало'),
            ('мало', 'поседевшие'),
        ]
        
        print("✓ CollocationFinder инициализирован")
    
    def _get_stopwords(self) -> set:
        """Стоп-слова для русского языка"""
        return {
            'и', 'во', 'не', 'что', 'он', 'я', 'как', 'а',
            'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'же',
            'вы', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот',
            'меня', 'еще', 'нет', 'о', 'ему', 'теперь', 'когда', 'даже',
            'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был',
            'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там',
            'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть',
            'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб',
            'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'будет', 'ж',
            'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем',
            'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее',
            'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при',
            'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше',
            'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много',
            'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой',
            'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им',
            'более', 'всегда', 'конечно', 'всю', 'между'
        }
    
    def split_sentences(self, text: str) -> List[str]:
        """Разбивает текст на предложения"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def preprocess_sentence(self, sentence: str) -> List[str]:
        
        sentence = sentence.lower()
    
        sentence = re.sub(r'[^\w\s]', ' ', sentence)
    
        words = sentence.split()
    
        filtered_words = []
        for w in words:
            if len(w) <= 1 and w not in self.prepositions:
                continue
            filtered_words.append(w)
    
        return filtered_words    
    
    def is_good_collocation(self, word1: str, word2: str, freq: int) -> bool:
        
        if freq >= 2:
            return True
        
        # Прилагательное + существительное
        if word2.endswith(('а', 'я', 'о', 'е', 'и', 'ы', 'у', 'ю')) and not word1.endswith(('а', 'я')):
            return True
        
        # Глагол + существительное
        if word1.endswith(('ть', 'ет', 'ит', 'ют', 'ят', 'л', 'ла', 'ли')):
            return True
        
        # Существительное + глагол
        if word2.endswith(('ть', 'ет', 'ит', 'ют', 'ят', 'л', 'ла', 'ли')):
            return True
        
        # Наречие + глагол
        if word1 in self.adverbs and word2.endswith(('ть', 'ет', 'ит', 'ют', 'ят')):
            return True
        
        return False
    
    def is_meaningful_collocation(self, word1: str, word2: str, freq: int, dice: float) -> bool:
        
        if freq >= 2:
            return True
        
        if (word1, word2) in self.bad_patterns:
            return False
        
        if dice < 0.6:
            return False
        
        if word1 in self.boring_words and word2 in self.boring_words:
            return False
                
        if word1 in self.prepositions or word2 in self.prepositions:
            return False
        
        if word1 in self.conjunctions or word2 in self.conjunctions:
            return False
        
        if (word1 in self.boring_words or word2 in self.boring_words) and freq == 1:
            return False
        
        if word1 in self.pronouns and word2.endswith(('ть', 'ет', 'ит', 'ют', 'ят')):
            if freq == 1:
                return False
        
        if word2 in self.pronouns:
            return False
        
        if word1 in self.adverbs and not word2.endswith(('ть', 'ет', 'ит', 'ют', 'ят')):
            return False
        
        return True
    
    def find_collocations(self, text: str, min_freq: int = 2) -> Dict:        
        try:            
            sentences = self.split_sentences(text)
            print(f"Найдено предложений: {len(sentences)}")
            
            all_words = []
            
            for sent_num, sentence in enumerate(sentences):
                print(f"Предложение {sent_num + 1}: {sentence}")
                words = self.preprocess_sentence(sentence)
                
                if words:
                    all_words.extend(words)
                    print(f"  -> слова в предложении: {words}")
            
            print(f"ВСЕ СЛОВА: {all_words}")
            
            if len(all_words) < 2:
                return {
                    'total_words': len(all_words),
                    'unique_words': 0,
                    'total_bigrams': 0,
                    'collocations': []
                }
            
            unigram_freq = Counter(all_words)
            N = len(all_words)
            
            print(f"Частоты слов: {dict(unigram_freq)}")
            
            bigram_dict = {}
            trigram_dict = {}
            
            for sentence in sentences:
                words = self.preprocess_sentence(sentence)
                print(f"  обработка предложения: {words}")
                
                for i in range(len(words)-1):
                    word1 = words[i]
                    word2 = words[i+1]
                    
                    key = f"{word1} {word2}"
                    
                    if key not in bigram_dict:
                        bigram_dict[key] = {
                            'freq': 0,
                            'word1': word1,
                            'word2': word2
                        }
                    
                    bigram_dict[key]['freq'] += 1
                
                for i in range(len(words)-2):
                    word1 = words[i]
                    word2 = words[i+1]
                    word3 = words[i+2]
                    
                    if word2 in self.prepositions:
                        key = f"{word1} {word2} {word3}"
                        
                        if key not in trigram_dict:
                            trigram_dict[key] = {
                                'freq': 0,
                                'words': (word1, word2, word3)
                            }
                        
                        trigram_dict[key]['freq'] += 1
            
            print(f"Найдено уникальных биграмм: {len(bigram_dict)}")
            print(f"Найдено уникальных триграмм: {len(trigram_dict)}")
            
            results = []
            
            for key, data in trigram_dict.items():
                freq_ab = data['freq']
                
                if freq_ab < min_freq:
                    continue
                
                results.append({
                    'bigram': key,
                    'frequency': freq_ab,
                    'pmi': 0,
                    't_score': 0,
                    'dice': 0
                })
            
            for key, data in bigram_dict.items():
                word1 = data['word1']
                word2 = data['word2']
                freq_ab = data['freq']
                
                skip = False
                for t_key in trigram_dict.keys():
                    if word1 in t_key and word2 in t_key:
                        skip = True
                        break
                
                if skip:
                    continue
                
                if freq_ab < min_freq:
                    continue
                
                if not self.is_good_collocation(word1, word2, freq_ab):
                    continue
                
                freq_a = unigram_freq.get(word1, 0)
                freq_b = unigram_freq.get(word2, 0)
                
                if freq_a == 0 or freq_b == 0:
                    continue
                
                pmi = 0
                if N > 0 and freq_a > 0 and freq_b > 0 and freq_ab > 0:
                    p_ab = freq_ab / N
                    p_a = freq_a / N
                    p_b = freq_b / N
                    pmi = math.log2(p_ab / (p_a * p_b))
                
                t_score = 0
                if N > 0 and freq_ab > 0:
                    expected = (freq_a * freq_b) / N
                    t_score = (freq_ab - expected) / math.sqrt(freq_ab)
                
                dice = 0
                if (freq_a + freq_b) > 0:
                    dice = (2 * freq_ab) / (freq_a + freq_b)
                
                if not self.is_meaningful_collocation(word1, word2, freq_ab, dice):
                    continue
                
                results.append({
                    'bigram': key,
                    'frequency': freq_ab,
                    'pmi': round(pmi, 3),
                    't_score': round(t_score, 3),
                    'dice': round(dice, 3)
                })
            
            results.sort(key=lambda x: x['frequency'], reverse=True)
            
            print(f"Найдено коллокаций: {len(results)}")
            
            return {
                'total_words': len(all_words),
                'unique_words': len(unigram_freq),
                'total_bigrams': len(bigram_dict) + len(trigram_dict),
                'collocations': results
            }
            
        except Exception as e:
            print("!" * 50)
            print(f"ОШИБКА В АНАЛИЗЕ: {e}")
            import traceback
            traceback.print_exc()
            print("!" * 50)
            
            return {
                'total_words': 0,
                'unique_words': 0,
                'total_bigrams': 0,
                'collocations': [],
                'error': str(e)
            }