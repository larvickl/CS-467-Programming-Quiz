document.addEventListener('DOMContentLoaded', function() {
    const quizLinks = document.querySelectorAll('.quiz-link');
    
    const modalHTML = `
        <div id="quizModal" class="modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
            <div class="modal-content" style="background: white; margin: 15% auto; padding: 20px; width: 70%; max-width: 700px; border-radius: 5px; position: relative;">
                <span class="close" style="position: absolute; top: 10px; right: 10px; cursor: pointer; font-size: 28px; background: #f0f0f0; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">&times;</span>
                <div id="modalContent">Loading...</div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById('quizModal');
    const closeBtn = modal.querySelector('.close');
    const modalContent = document.getElementById('modalContent');
    
    quizLinks.forEach(function(link) {
        link.addEventListener('click', async function(event) {
            event.preventDefault();
            const quizId = this.getAttribute('data-quiz-id');
            
            modal.style.display = 'block';
            
            try {
                const response = await fetch(`/employer/quiz/${quizId}/results`);
                console.log('Response status:', response.status);
                
                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Failed to fetch quiz results - Status: ${response.status}, Response: ${errorText}`);
                }
                
                const data = await response.json();
                const sortedResults = data.results.sort((a, b) => parseFloat(b.score) - parseFloat(a.score));
                
                modalContent.innerHTML = `
                    <div class="table-responsive">
                        <h3>Quiz Participants (${sortedResults.length})</h3>
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    <th scope="col">Name</th>
                                    <th scope="col" class="text-center">Score</th>
                                    <th scope="col" class="text-center">Completion time</th>
                                    <th scope="col" class="text-center">Grade</th>
                                    <th scope="col" class="text-end">Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${sortedResults.map(result => `
                                    <tr>
                                        <td>${result.name}</td>
                                        <td class="text-center fw-bold">${result.score}%</td>
                                        <td class="text-center">${result.timeTaken}</td>
                                        <td class="text-center">${result.gradeElem}</td>
                                        <td class="text-end">${result.completionDate}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                    <div class="card mt-4">
                        <div class="card-body">
                            <h3 class="card-title">Quiz Overview</h3>
                            <div class="row g-3">
                                <div class="col-sm-6 col-md-3">
                                    <div class="fw-bold">Average Score:</div>
                                    ${data.overview.averageScore}%
                                </div>
                                <div class="col-sm-6 col-md-3">
                                    <div class="fw-bold">Completion Rate:</div>
                                    ${data.overview.completionRate}%
                                </div>
                                <div class="col-sm-6 col-md-3">
                                    <div class="fw-bold">Total Attempts:</div>
                                    ${data.overview.totalAttempts}
                                </div>
                                <div class="col-sm-6 col-md-3">
                                    <div class="fw-bold">Average Time:</div>
                                    ${data.overview.averageTimeTaken}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } catch (error) {
                modalContent.innerHTML = `
                    <div class="alert alert-danger">
                        <h3 class="h5">Error Loading Quiz Results</h3>
                        <p class="mb-0">Details: ${error.message}</p>
                    </div>
                `;
                console.error('Detailed error:', error);
            }
        });
    });
    
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});