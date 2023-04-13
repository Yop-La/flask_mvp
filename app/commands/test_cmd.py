import os
import click
from flask.cli import with_appcontext
import shutil


@click.command('test:wd2')
@with_appcontext
def test_wd2():
    import os
    import time

    total_records_sent = 0
    start_time = time.time()
    batch_size = 10
    rate = int(os.getenv('RATE', 10))
    sleep_time=0
    csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
    videos_to_save = []
    for csv_file in csv_files:

        import pandas as pd
        from db import db
        from models.videos import VideoModel

        country_code = csv_file[:2]

        # Chargement des données CSV en utilisant Pandas
        print('reading data/%s' % csv_file)
        df = pd.read_csv('data/%s' % csv_file, dtype={
            'category_id': int,
            'views': int,
            'likes': int,
            'dislikes': int,
            'comment_count': int,
            'comments_disabled': bool,
            'ratings_disabled': bool,
            'video_error_or_removed': bool
        }, encoding='iso-8859-1')
        df=df.drop_duplicates(subset=['video_id','trending_date'])






        # Pour chaque ligne de données, créer un nouvel objet VideoModel et l'enregistrer dans la base de données
        for _, row in df.iterrows():

            video = VideoModel(
                video_id=row['video_id'],
                trending_date=row['trending_date'],
                title=row['title'],
                channel_title=row['channel_title'],
                category_id=int(row['category_id']),
                publish_time=row['publish_time'],
                tags=row['tags'],
                views=int(row['views']),
                likes=int(row['likes']),
                dislikes=int(row['dislikes']),
                comment_count=int(row['comment_count']),
                thumbnail_link=row['thumbnail_link'],
                comments_disabled=bool(row['comments_disabled']),
                ratings_disabled=bool(row['ratings_disabled']),
                video_error_or_removed=bool(row['video_error_or_removed']),
                description=row['description'],
                country_code=country_code
            )
            videos_to_save.append(video)
            elapsed_time = time.time() - start_time
            if len(videos_to_save) >= batch_size:
                print('--')
                db.session.bulk_save_objects(videos_to_save)
                db.session.commit()
                total_records_sent = total_records_sent + len(videos_to_save)
                print('saving videos: %s' % total_records_sent)
                videos_to_save = []

                elapsed_time = time.time() - start_time

                real_rate = total_records_sent / elapsed_time

                print('real rate: %s' % real_rate)
                print('rate: %s' % rate)



                if real_rate > rate:

                    sleep_time = batch_size / (real_rate - rate)
                    print('elapsed time: %s' % elapsed_time)
                    print('total records sent: %s' % total_records_sent)
                    print('records per second: %s' % (total_records_sent / elapsed_time))
                    print('sleep time: %s' % sleep_time)
                    time.sleep(sleep_time)












        print(csv_file)

    db.session.bulk_save_objects(videos_to_save)
    db.session.commit()
    print("running test:wd2 job")
    return