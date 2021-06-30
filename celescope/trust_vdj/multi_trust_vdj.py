from celescope.trust_vdj.__init__ import __ASSAY__
from celescope.tools.multi import Multi


class Multi_trust_vdj(Multi):

    def convert(self, sample):
        step = 'convert'
        arr = self.fq_dict[sample]
        cmd_line = self.get_cmd_line(step, sample)
        cmd = (
           f'{cmd_line} '
           f'--fq1 {arr[0]} --fq2 {arr[1]} '
        )
        self.process_cmd(cmd, step, sample, m=5, x=1)


    def mapping(self, sample):
        step = 'mapping'
        cmd_line = self.get_cmd_line(step, sample)
        fq = f'{self.outdir_dic[sample]["convert"]}/{sample}_2.fq'
        cmd = (
            f'{cmd_line} '
            f'--fq {fq} '
        )
        self.process_cmd(cmd, step, sample,  m=self.args.starMem, x=self.args.thread)


    def count(self, sample):
        step = 'count'
        cmd_line = self.get_cmd_line(step, sample)
        bam_file = f'{self.outdir_dic[sample]["mapping"]}/{sample}_Aligned.sortedByCoord.out.bam'
        fq1 = f'{self.outdir_dic[sample]["convert"]}/{sample}_1.fq'
        cmd = (
            f'{cmd_line} '
            f'--bam_file {bam_file} '
            f'--fq1 {fq1} '
        )
        self.process_cmd(cmd, step, sample, m=5, x=2)


    def assemble(self, sample):
        step = 'assemble'
        cmd_line = self.get_cmd_line(step, sample)
        fq1 = f'{self.outdir_dic[sample]["count"]}/{sample}_mapped_R1.fq'
        fq2 = f'{self.outdir_dic[sample]["count"]}/{sample}_mapped_R2.fq' 
        cmd = (
            f'{cmd_line} '
            f'--fq1 {fq1} '
            f'--fq2 {fq2} '
        )
        self.process_cmd(cmd, step, sample, m=30, x=self.args.thread)



def main():
    multi = Multi_trust_vdj(__ASSAY__)
    multi.run()

if __name__ == '__main__':
    main()
