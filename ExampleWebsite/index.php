<?php 
    $db = new SQLite3('database/jobs.db');

    /*
    if ($_SERVER['REQUEST_METHOD'] === 'POST'){
        if (isset($_POST['mark-as-applied'])){
            echo "yes";
            $job_id = $_POST['id'];
            #This prepares the sql statement without executing it so that we can bind values
            $statement = $db->prepare("UPDATE jobs SET status = 'applied' WHERE id = :id");
            #Replace _id with the value of job_id
            $statement->bindValue(':id', $job_id, SQLITE3_INTEGER);
            #Now we can execute the statement
            $statement->execute();
        }

        header('Location: index.php');
    }
    */

    $result = $db->query("SELECT * FROM jobs ORDER BY SUBSTR(date,10,-4) DESC, SUBSTR(date,4,5) DESC, SUBSTR(date,1,2) DESC");

    $jobs = [];
    // Iterate over each row until none are left and store the values in the jobs array
    while($row = $result->fetchArray(SQLITE3_ASSOC)){
    
        $jobs[] = $row;
    }


?>

<!DOCTYPE html>
<html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
        <title>Code Game Crawler</title> 
    </head>

    <body>
        <main>
            <div class="container py-5 text-center">
                <h1 class="display-5 fw-bold">Code Game Crawler</h1>
                <p class="lead text-muted">
                    A collection of automatically aggregated programming jobs for game developers. 
                </p>
            </div>
          
            <!--Job board table-->
            <div>
                <table id ="job-board" class="table table-striped table-hover text-center w-75 mx-auto">
                    <thead>
                        <tr>
                            <th>Job Title</th>
                            <th>Company</th>
                            <th>Date Posted</th>
                            <th>Location</th>
                            <th>Link</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <?php foreach ($jobs as $job){?>
                            <tr>
                                <td><?php echo $job['title'] ?></td>
                                <td><?php echo $job['company'] ?></td>
                                <td><?php echo $job['date'] ?></td>
                                <td><?php echo $job['location'] ?></td>
                                <td><a href="<?=$job['link']?>" class="btn btn-outline-primary" target="_blank">View</a></td>
                            </tr>
                        <?php } ?>
                    </tbody>
                </table>
            </div>

        </main>

        <footer>
            <h3 class="text-center">Currently sourced from</h3>
            <p class="text-center"><i><a href="https://workwithindies.com" target="_blank">Work With Indies</a></i></p>
        </footer>

    </body>
</html>

