Instructions to run the End2End Model in the terminal:
---

1. Cd Downloads (file location of wpi_id_rsa)
2. chmod 400 wpi_id_rsa
3. ssh -i wpi_id_rsa wpi-project@35.221.34.129
4. cd vanand (my folder in the server)
5. git clone https://github.com/dalab/end2end_neural_el
6. cd end2end_neural_el
7. python3 -m pip install virtualenv
8. python3 -m virtualenv end2end_neural_el_env
9. source end2end_neural_el_env/bin/activate
10. pip install -r requirements.txt
11. Download data.zip file and place in downloads folder: (back in local) https://drive.google.com/file/d/1OSKvIiXHVVaWUhQ1-fpvePTBQfgMT6Ps/view?usp=sharing
12. scp -i wpi_id_rsa data.zip wpi-project@35.221.34.129:vanand/end2end_neural_el/
13. unzip vanand/end2end_neural_el/data.zip
14. Download GoogleNews-vectors-negative300.bin.gz file and place in downloads folder: (back in local) https://code.google.com/archive/p/word2vec/ 
15. unzip the gz file in local, then place in remote server
16. scp -i wpi_id_rsa GoogleNews-vectors-negative300.bin wpi-project@35.221.34.129:vanand/end2end_neural_el/data/basic_data/wordEmbeddings/Word2Vec
17. cd vanand/end2end_neural_el/code
18. python -m preprocessing.prepro_aida
19. python -m preprocessing.prepro_other_datasets
20. python -m preprocessing.prepro_util (shows the training scores for each data set)
21. **For EL: (shows the testing scores)**
python -m model.evaluate --training_name=base_att_global  --experiment_name=paper_models --entity_extension=extension_entities  --el_datasets=aida_dev_z_aida_test_z_aida_train_z_ace2004_z_aquaint_z_clueweb_z_msnbc_z_wikipedia    --el_val_datasets=0  --ed_datasets=""  --ed_val_datasets=0   --all_spans_training=True
22. **For ED:**
python -m model.evaluate --training_name=base_att_global  --experiment_name=paper_models --entity_extension=extension_entities  --ed_datasets=aida_dev_z_aida_test_z_aida_train_z_ace2004_z_aquaint_z_clueweb_z_msnbc_z_wikipedia    --ed_val_datasets=0  --el_datasets=""  --el_val_datasets=0

scp -i wpi_id_rsa BTdata.zip wpi-project@35.221.34.129:vanand/end2end_neural_el/data/basic_data/test_datasets/wned-datasets **(all one line -> to import BT data from local into remote server)**

**export file from remote server to local**:
scp user@remote.host1:/var/tmp/host1.file.zip /local/path/dir

**Basis Technology Github:**
https://github.com/basis-technology-corp/wpi-gqp-2020 

**End to End Model Instructions:**
https://github.com/dalab/end2end_neural_el
