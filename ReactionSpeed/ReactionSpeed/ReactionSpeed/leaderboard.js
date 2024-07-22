function showLeaderboard() {
    fetch('reaction_speeds.csv')  
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(text => {
            const lines = text.split('\n').filter(line => line);
            const milliseconds = [];
            const accuracies = [];

           
            lines.forEach(line => {
                const [time, accuracy] = line.split(',');
                milliseconds.push(parseFloat(time));
                accuracies.push(parseFloat(accuracy));
            });

            //This will create our chart
            const ctx = document.getElementById('reactionChart').getContext('2d');
            new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Reaction Times vs Accuracy',
                        data: milliseconds.map((time, index) => ({ x: time, y: accuracies[index] })),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Reaction Time (ms)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Accuracy'
                            },
                            beginAtZero: true,
                            ticks: {
                                callback: (value) => value.toFixed(2)
                            }
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}


showLeaderboard();
