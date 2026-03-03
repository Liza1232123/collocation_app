// Ждем полной загрузки страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log("Страница загружена, инициализация...");
    
    // Получаем элементы
    const textInput = document.getElementById('textInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const minFreqSelect = document.getElementById('minFreq');
    const wordCountSpan = document.getElementById('wordCount');
    const loadingDiv = document.getElementById('loading');
    const resultsDiv = document.getElementById('results');
    const saveBtn = document.getElementById('saveBtn');
    const saveMessage = document.getElementById('saveMessage');
    
    // Проверяем, что все элементы найдены
    if (!textInput) console.error("textInput не найден");
    if (!analyzeBtn) console.error("analyzeBtn не найден");
    if (!minFreqSelect) console.error("minFreqSelect не найден");
    
    // Счетчик слов
    if (textInput && wordCountSpan) {
        textInput.addEventListener('input', function() {
            const text = this.value;
            const words = text.trim().split(/\s+/).filter(w => w.length > 0);
            wordCountSpan.textContent = words.length + ' слов';
        });
    }
    
    // Анализ текста
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', async function() {
            console.log("Кнопка нажата");
            
            const text = textInput ? textInput.value.trim() : '';
            const minFreq = minFreqSelect ? minFreqSelect.value : '1';
            
            if (text.length < 10) {
                alert('Пожалуйста, введите больше текста');
                return;
            }
            
            console.log("Отправляем запрос с min_freq =", minFreq);
            
            // Показываем загрузку
            if (loadingDiv) loadingDiv.classList.remove('hidden');
            if (resultsDiv) resultsDiv.classList.add('hidden');
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        min_freq: parseInt(minFreq)
                    })
                });
                
                const data = await response.json();
                console.log("Получены данные:", data);
                
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                // Показываем результаты
                displayResults(data);
                
            } catch (error) {
                console.error('Ошибка:', error);
                alert('Произошла ошибка при анализе');
            } finally {
                if (loadingDiv) loadingDiv.classList.add('hidden');
            }
        });
    }
    
    // Обработчики вкладок
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log("Вкладка нажата:", this.dataset.tab);
            
            // Убираем активный класс у всех вкладок
            tabBtns.forEach(b => b.classList.remove('active'));
            // Добавляем активный класс текущей вкладке
            this.classList.add('active');
            // Обновляем таблицу
            updateTable(this.dataset.tab);
        });
    });
    
    // Сохранение результатов
    if (saveBtn) {
        saveBtn.addEventListener('click', async function() {
            if (!window.currentData) return;
            
            const timestamp = new Date().toISOString().slice(0,19).replace(/:/g, '-');
            const filename = `collocations_${timestamp}.json`;
            
            try {
                const response = await fetch('/save', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        results: window.currentData,
                        filename: filename
                    })
                });
                
                const result = await response.json();
                
                if (saveMessage) {
                    saveMessage.textContent = '✅ ' + result.message;
                    saveMessage.style.color = '#28a745';
                    
                    setTimeout(() => {
                        saveMessage.textContent = '';
                    }, 3000);
                }
                
            } catch (error) {
                console.error('Ошибка при сохранении:', error);
                alert('Не удалось сохранить результаты');
            }
        });
    }
});

// Отображение результатов
function displayResults(data) {
    console.log("displayResults вызвана с данными:", data);
    
    // Обновляем статистику
    const totalWords = document.getElementById('totalWords');
    const uniqueWords = document.getElementById('uniqueWords');
    const totalBigrams = document.getElementById('totalBigrams');
    
    if (totalWords) totalWords.textContent = data.total_words || 0;
    if (uniqueWords) uniqueWords.textContent = data.unique_words || 0;
    if (totalBigrams) totalBigrams.textContent = data.total_bigrams || 0;
    
    // Сохраняем данные для вкладок
    window.currentData = data;
    
    // Показываем таблицу с сортировкой по PMI (по умолчанию)
    updateTable('pmi');
    
    const resultsDiv = document.getElementById('results');
    if (resultsDiv) resultsDiv.classList.remove('hidden');
}

// Обновление таблицы в зависимости от выбранной вкладки
function updateTable(sortBy) {
    console.log("updateTable вызвана с sortBy =", sortBy);
    
    if (!window.currentData || !window.currentData.collocations) {
        console.log("Нет данных для отображения");
        return;
    }
    
    let collocations = [...window.currentData.collocations];
    console.log(`Сортируем по ${sortBy}, всего ${collocations.length} записей`);
    
    // Сортируем по выбранной метрике
    switch(sortBy) {
        case 'pmi':
            collocations.sort((a, b) => b.pmi - a.pmi);
            break;
        case 't_score':
            collocations.sort((a, b) => b.t_score - a.t_score);
            break;
        case 'dice':
            collocations.sort((a, b) => b.dice - a.dice);
            break;
        case 'frequency':
            collocations.sort((a, b) => b.frequency - a.frequency);
            break;
    }
    
    // Генерируем HTML для таблицы
    const tbody = document.getElementById('tableBody');
    if (!tbody) {
        console.error("tableBody не найден");
        return;
    }
    
    if (collocations.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Нет результатов для отображения</td></tr>';
    } else {
        tbody.innerHTML = collocations.map((item, index) => {
            // Проверяем, что все значения существуют
            const frequency = item.frequency || 0;
            const pmi = item.pmi || 0;
            const t_score = item.t_score || 0;
            const dice = item.dice || 0;
            
            return `
                <tr>
                    <td>${index + 1}</td>
                    <td><strong>${item.bigram || '—'}</strong></td>
                    <td>${frequency}</td>
                    <td>${pmi}</td>
                    <td>${t_score}</td>
                    <td>${dice}</td>
                </tr>
            `;
        }).join('');
    }
}