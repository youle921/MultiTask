�T�v
----
Hypervolume���v�Z����v���O����. �����w�肪�Ȃ��ꍇ��, �ő剻�������肷��. 
�ǂݍ��񂾉��W���ɗ�����܂܂�Ă��Ă�, �Q�Ɠ_�����D�z���Ȃ������܂܂�Ă��Ă�, �d�������܂܂�Ă��Ă������������悤�ɍ���Ă���. 


�t�@�C������
-------------
args4j/  -- Java�̃R�}���h������̓��C�u����. Licensed under MIT by Kohsuke Kawaguchi and other contributors. http://args4j.kohsuke.org/
sampledata/ -- �v���O��������m�F�p�̃f�[�^. 
hv.bat -- Hypervolume�v�Z�v���O����, CUI����.
hv-gui.bat -- Hypervolume�v�Z�v���O����, GUI����.
indicator.jar -- Hypervolume�v�Z�v���O�����{��.
readme.txt -- ���̃t�@�C��.
reference.csv -- hv-gui.bat�ŎQ�Ɠ_���w�肷��t�@�C��.


�g�p���@
---------
GUI: 
�t�@�C����hv-gui.bat��D&D. �Q�Ɠ_��reference.csv�Ɏw�肷��. �Q�Ɠ_�̐���1�̂�. 
�ŏ���, exact-calculation���[�h�Ȃǂ�, hv-gui.bat������������Ȃ肵�đΉ�����. 

CUI: 
hv.bat�����s. �����Ȃ��Ŏ��s�����, �p�����[�^�̐��������\�������.
�t�@�C������+���w�肷���, �W�����͂���f�[�^��ǂݍ���. �Ǝ��t�H�[�}�b�g���g�p�������ꍇ��, ����𗘗p���ĕϊ��v���O���������܂���ׂ�.


�Ή��f�[�^�t�H�[�}�b�g
-----------------------
* csv�t�H�[�}�b�g
#�Ŏn�܂�s�̓R�����g. 
���W���̋�؂��, 1�ȏ�̋󔒍s. 
�w�b�_�ɂ͑Ή����Ă��Ȃ�. �f���~�^�̓^�u�̂ݎg�p�\. 


* �Ǝ��t�H�[�}�b�g MTD (Markup Table Data)
�g���q�͕K��mtd. 
##�Ŏn�܂�s�̓R�����g. 
#�Ŏn�܂�s��Markup����. 

�ړI�֐��̒l�������n�߂�O�Ɉȉ��̓��e���L���Ă������� (���s��). 
#nObjectives: [�ړI��]
#nTrials: [���s�� (���W���̐�)]
#isMaximize: [Boolean]
#nonDominated: [Boolean]
#nonOverlapping: [Boolean]

�e���W���̑O�ɂ�, ���̐���
#nSols: [number]
�̌`���ŏ�������. ���W���̋�؂��1�ȏ�̋󔒍s.

�ړI���ȊO�͏ȗ��\. isMaximize�ȗ�����True���w�肵�����̂Ƃ݂Ȃ����. 
nonDominated, nonOverlapping��2�͏ȗ���, False���w�肵�����̂Ƃ݂Ȃ�. 
�̌Q�T�C�Y�����ɑ傫���Ƃ���, �������菜�������Ɏ��Ԃ�������. �傫���f�[�^�������Ƃ��͗\�ߗ����d��������菜��, �����̃t���O�𗧂ĂĂ����Ɨǂ�. �����W���ł͂Ȃ��̂�nonDominated��true�ł��铙, �R���܂܂�Ă����ꍇ, ���ʂ̐������͕ۏ؂���Ȃ�. 

* �Ǝ�csv���ǂ��t�H�[�}�b�g (sampledata/test.dat)
1�s��: �ړI��
2�s��: ���s�� (���W���̐�)
�Ȍ�, 
���̐�
�ړI�֐�
...
�̌J��Ԃ�.


�I�v�V�����ɂ���
-------------------
* verbose
Hypervolume�̕��ςƕW���΍����^�u��؂�ŏo�͂���. 

* all
�e���W����Hypervolume��1�s���Ƃɕ\������.

* very-verbose
verbose�̑O��, ����, �W���΍�, �󔒍s���\������. 

* exact-calculation
�ړI�֐����S�Đ����l�����ꍇ, ���{��������p����Hypervolume�������Ɍv�Z����. 
(�ʏ�̃��[�h�ł�, 64bit���x��, �L������15�����x)
�����I��very-verbose���[�h�ɂȂ�. �W���΍��̑���ɕW�{���U��\������. 

* format (csv/mtd)
�W�����͂���ǂݍ��񂾃f�[�^�̃t�H�[�}�b�g���w�肷�� (csv or mtd). 
�f�t�H���g��mtd. 

* sort
�����̃t�@�C���������ɗ^����ꂽ�ꍇ, �t�@�C�����\�[�g���Ă��猋�ʂ�\������. �t�@�C�����ɐ������܂܂�Ă���ꍇ��, �������ł͂Ȃ�, ���l�̑召���l�����Č��ʂ�\������. 

��:
> hv.bat -r 0 kp10_hv10.mtd kp2_hv2.mtd kp5_hv5.mtd
10.0	2.0	5,0
> hv.bat -s -r 0 kp10_hv10.mtd kp2_hv2.mtd kp5_hv5.mtd
2.0	5,0	10.0


�ŏ������ɂ���
-------------------
�R�}���h���C���I�v�V����
* minimize �ŏ������Ƃ��Ĉ���. �ړI�֐��ƎQ�Ɠ_��-1�{����. 
* negate �ő剻�ŏ����֌W�Ȃ�, �ړI�֐��ƎQ�Ɠ_��S��-1�{����. 

MTD��isMaximize = false�Ƃ��Ă�, �ړI�֐��ƎQ�Ɠ_��-1�{�����. 

### �����ɂ���
minimize, isMaximize = false�͍ŏ������Ƃ݂Ȃ�. �������w�肳��Ă�-1�{�͈�x����. 
negate��, minimize�ȂǂɊ֌W�Ȃ�-1�{����. minimize��isMaximize = false�Ɠ����Ɏg�p�����ꍇ, �ő剻���Ɠ����ɂȂ�. 

�������v�Z������:
hv.bat -r 15e3 mokp.csv
hv.bat -r 1.1 -n dtlz2.csv
hv.bat -r 1.1 -m dtlz2.csv
hv.bat -r 1.1 dtlz2.mtd			// isMaximize = false���w�肳��Ă���
hv.bat -r 1.1 -m dtlz2.mtd		// isMaximize = false���w�肳��Ă���


�Q�Ɠ_�ɂ���
---------------
�R���}��؂�Ŏw�肷��. �ړI���ɖ����Ȃ��ꍇ�͌J��Ԃ����.
...�ŏI���ꍇ��, �����E���䐔����g�p����.  �����Ƒ�񍀂��^�����Ă���ꍇ�͓�������, ��O�����^�����Ă���ꍇ��
�����I�ɓ����E���䐔�񂩔��f����. 

�� (4�ړI):
-r 0  ==> (0 0 0 0)
-r "0,1" == > (0 1 0 1)
-r "3,5,7" ==> (3 5 7 3)
-r "3,5,7,	 9" ==> (3 5 7 9)
-r 10 -m ==> (-10 -10 -10 -10)
-r 3,5,... ==> (3, 5, 7, 9)
-r 3,5,7,... ==> (3, 5, 7, 9)
-r "3,5,7,9,..." ==> (3, 5, 7, 9)
-r 10,100,... ==> (10, 100, 190, 280)
-r 10,100,1000,... ==> (10, 100, 1000, 10000)
