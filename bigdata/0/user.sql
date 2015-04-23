.open tmp.db
.mode csv
.separator "\t"
.import clinical.tsv clinical
.import ssm_open.tsv ssm_open
CREATE TABLE distinct_ssm AS SELECT DISTINCT icgc_donor_id, project_code, chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele FROM ssm_open;
CREATE TABLE fin_clinical AS SELECT icgc_donor_id, project_code, donor_age_at_diagnosis, donor_age_at_enrollment, donor_tumour_stage_at_diagnosis, tumour_grade FROM (SELECT DISTINCT icgc_donor_id, project_code, donor_age_at_diagnosis, donor_age_at_enrollment, donor_tumour_stage_at_diagnosis, tumour_grade FROM clinical) GROUP BY icgc_donor_id, project_code, donor_age_at_diagnosis, donor_age_at_enrollment, donor_tumour_stage_at_diagnosis, tumour_grade HAVING tumour_grade=max(tumour_grade);
CREATE TABLE big_comb AS SELECT * FROM distinct_ssm LEFT OUTER JOIN fin_clinical USING (icgc_donor_id, project_code);
CREATE TABLE final_result AS SELECT chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele, count() AS patient_number, max(donor_age_at_enrollment) AS max_donor_age_at_enrollment, min(donor_age_at_enrollment) AS min_donor_age_at_enrollment, avg(donor_age_at_enrollment) AS avg_donor_age_at_enrollment FROM big_comb GROUP BY chromosome, chromosome_start, chromosome_end, chromosome_strand, assembly_version, reference_genome_allele, mutated_from_allele, mutated_to_allele ORDER BY patient_number DESC;

ALTER TABLE final_result ADD COLUMN tumour_grade TEXT;

ALTER TABLE final_result ADD COLUMN donor_tumour_stage_at_diagnosis TEXT;