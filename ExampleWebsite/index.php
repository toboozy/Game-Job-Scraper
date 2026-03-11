<?php 

    //Jobs is the array we'll use to display the job board
    //It's refreshed each time the page loads and may change depending on search queries
    $jobs = [];

    //Connect to the database
    $db = new SQLite3('database/jobs.db');

    $result = [];

    if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    
        if (isset($_GET['query'])){

            //Raw input from the user
            $searchQuery = $_GET['query'];
            //Sanatize the input
            $searchQuery = strtolower($searchQuery);
            $searchQuery = trim($searchQuery);
            //Convert the search query to an array so we can check each word individually
            $queries = explode(" ", $searchQuery);


            foreach($queries as $q){

                $search = '%' . $q . '%';
                $stmt = $db->prepare("SELECT * FROM jobs WHERE title LIKE :search");
                $stmt->bindValue(':search', $search, SQLITE3_TEXT);
                $result = $stmt->execute();

                // Iterate over each row until none are left and store the values in the jobs array
                while($row = $result->fetchArray(SQLITE3_ASSOC)){
                    
                    $jobs[] = $row;

                }

            }
        }
        else{
        
            //Default query - Just get everything from the database
            $result = $db->query("SELECT * FROM jobs ORDER BY SUBSTR(date,10,-4) DESC, SUBSTR(date,4,5) DESC, SUBSTR(date,1,2) DESC");

            // Iterate over each row until none are left and store the values in the jobs array
            while($row = $result->fetchArray(SQLITE3_ASSOC)){
    
                $jobs[] = $row;

            }
        }
    }

?>

<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
        <link href="style.css" rel="stylesheet">
        <title>Code Game Crawler</title> 
    </head>

    <body>
        <main>
            <div class="container py-5 text-center">
                <h1 class="display-5 fw-bold"><a href="https://www.mattmuller.dev/" target="_blank">MattMuller.Dev's Job Board</a></h1>
                <h2 class="lead text-muted">
                    A collection of automatically aggregated programming jobs for game developers. 
                </h2>
            </div>

            <!--Search-->
            <!-- I'm using a form with GET for usability as the searches shouldn't need to be private and it retains a paper trail-->
            <div class="container mb-5 text-center">
                <form action="/" method="GET">
                    <div class="row w-50 mx-auto">
                        <div class="col-9 mx-auto">
                            <label for="query" class="visually-hidden">Search</label>
                            <input id="query" name="query" type="text" class="form-control" placeholder="Search Job Title..."></> 
                        </div>
                        <div class="col mx-auto">
                            <button type="submit" class="btn btn-primary w-100">Search</button>
                        </div>
                    </div>
                </form>
            </div>

            <div class="w-50 mx-auto">
                <?php foreach ($jobs as $job){ ?>

                    <div class="card h-100 mb-3 shadow-sm">
                        <a class="card-body d-flex flex-column stretched-link text-decoration-none" href="<?= $job['link'] ?>" target="_blank">
                            <div class="row">
                                <div class="mx-auto">

                                    <h3 class="card-title">
                                        <?= htmlspecialchars($job['title']) ?>
                                    </h3>

                                    <p class="text-muted small mb-2">
                                        <?= htmlspecialchars($job['company']) ?> • <?= htmlspecialchars($job['location']) ?> <?php if (isset($job['date'])){?>• Posted: <?php echo $job['date'] ?><?php }?>  
                                        
                                        <?php if (isset($job['date'])){
                                        
                                            if (strtotime($job['date']) > strtotime('-3 days')){ ?>
                                            <span class="badge bg-success ms-2 align-text-top">New</span>
                                        
                                        <?php } //if date is within 3 days
                                        } //if isset?>
                                    </p>

                                </div>
                            </div>
                        </a>
                    </div>
                <?php } ?>
            </div>

        </main>

        <footer>
            <h3 class="text-center">Currently sourced from</h3>
            <ul class="text-center list-unstyled">
                <li><i><a href="https://workwithindies.com" target="_blank">Work With Indies</a></i></li>
                <li><i><a href="https://gameloft.com" target="_blank">Gameloft</a></i></li>
                <li><i><a href="https://www.riotgames.com" target="_blank">Riot Games</a></i></li>
            </ul>
        </footer>

    </body>
</html>

