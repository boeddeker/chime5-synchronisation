from nt.utils.process_caller import run_process
from nt.database.chime5 import session_dataset_mapping


def main(
        session="S03",
        dataset="train",
):
    chime5_corpus = './CHiME5'
    audio_dir = f'{chime5_corpus}/audio'
    aligned_dir = "./transcriptions_aligned"
    align_data = "./align_data"

    # chime5_corpus=./CHiME5
    #
    # session="S03"     # The session to be aligned
    # dataset="train"   # The session's dataset. Can be 'train' or 'dev'
    #
    #
    # ##### Shouldn't need to edit anything beyond this point. #####
    #
    # audio_dir=${chime5_corpus}/audio
    #
    # aligned_dir="./transcriptions_aligned"
    # align_data="./align_data"

    run_process([
        'python3',
        'estimate_alignment.py',
        '--sessions', f'{session}',
        f'{audio_dir}/{dataset}',
        f'{align_data}/first_pass',
    ], stdout=None, stderr=None)
    run_process([
        'python3',
        'estimate_alignment.py',
        '--refine',
        f'{align_data}/first_pass',
        '--sessions', f'{session}',
        f'{audio_dir}/{dataset}',
        f'{align_data}/refined',
    ], stdout=None, stderr=None)
    run_process([
        'python3',
        'align_transcription.py',
        '--sessions', f'{session}',
        f'{align_data}/refined',
        f'{chime5_corpus}/transcriptions/{dataset}',
        f'{aligned_dir}'
    ], stdout=None, stderr=None)

    # Perform the course alignment pass (slowest step)
    # python3 estimate_alignment.py --sessions "$session" "$audio_dir"/"$dataset" "$align_data"/first_pass

    # Peform the alignment refinement pass
    # python3 estimate_alignment.py --refine "$align_data"/first_pass  --sessions "$session" "$audio_dir"/"$dataset"  "$align_data"/refined

    # Apply the alignment to the transcript file
    # python3 align_transcription.py --sessions "$session"  "$align_data"/refined "$chime5_corpus"/transcriptions/"$dataset" "$aligned_dir"

    # View the alignment
    # python3 view_alignments.py  --sessions "$session" "$align_data"/refined


if __name__ == '__main__':
    for session, dataset in session_dataset_mapping.items():
        main(session, dataset)
